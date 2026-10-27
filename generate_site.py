#!/usr/bin/env python3
"""
Generate the website's content from data.json.

Fills the marked regions of index.html (<!-- gen:name --> ... <!-- /gen:name -->)
so the page reads fully without JavaScript, and writes the files crawlers and
AI agents look for: llms.txt, resume.md, resume.txt, resume.json (JSON Resume),
robots.txt and sitemap.xml. Standard library only. Run ./build.sh.
"""

import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MONTHS = {m: i for i, m in enumerate(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}

AI_CRAWLERS = [
    'GPTBot', 'ChatGPT-User', 'OAI-SearchBot', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot',
    'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'CCBot',
]


def strip(text):
    """Drop inline HTML (data.json uses <br> in a few places)"""
    return re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>', ' ', str(text or ''), flags=re.I))


def esc(text):
    return html.escape(strip(text), quote=True)


def iso_date(part):
    """'Feb 2026' -> '2026-02', '2023' -> '2023', 'Present' -> None"""
    part = part.strip()
    m = re.fullmatch(r'([A-Z][a-z]{2}) (\d{4})', part)
    if m:
        return '%s-%02d' % (m.group(2), MONTHS[m.group(1)])
    return part if re.fullmatch(r'\d{4}', part) else None


def date_range(text):
    parts = re.split(r'\s+[–-]\s+', text)
    return iso_date(parts[0]), iso_date(parts[-1])


def links(data):
    p = data['personal']
    return {
        'site': p['websiteUrl'].rstrip('/'),
        'linkedin': 'https://www.linkedin.com/in/%s' % p['linkedin'],
        'github': 'https://github.com/%s' % p['github'],
    }


# ---------- index.html regions ----------

def html_regions(data):
    p, now, ed = data['personal'], data['experience'][0], data['education']
    url = links(data)
    name = '%s %s' % (p['firstName'], p['lastName'])
    summary = esc(data['tagline'])

    ld = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': name,
        'givenName': p['firstName'],
        'familyName': p['lastName'],
        'jobTitle': p['title'],
        'description': strip(data['about']),
        'url': url['site'] + '/',
        'email': 'mailto:' + p['email'],
        'address': {'@type': 'PostalAddress', 'addressLocality': p['location'].split(',')[0].strip(),
                    'addressRegion': p['location'].split(',')[-1].strip(), 'addressCountry': 'US'},
        'worksFor': {'@type': 'Organization', 'name': now['company'], 'description': strip(now.get('tagline'))},
        'alumniOf': {'@type': 'CollegeOrUniversity', 'name': ed['school']},
        'knowsAbout': data['skills']['technical'] + data['skills']['leadership'],
        'sameAs': [url['linkedin'], url['github']],
    }
    head = '\n'.join([
        '<meta name="description" content="%s">' % summary,
        '<meta property="og:type" content="profile">',
        '<meta property="og:title" content="%s, %s">' % (esc(name), esc(p['title'])),
        '<meta property="og:description" content="%s">' % summary,
        '<meta property="og:url" content="%s/">' % url['site'],
        '<link rel="canonical" href="%s/">' % url['site'],
        '<link rel="alternate" type="text/plain" href="llms.txt" title="Summary for AI agents">',
        '<link rel="alternate" type="text/markdown" href="resume.md" title="Resume (Markdown)">',
        '<link rel="alternate" type="application/json" href="resume.json" title="Resume (JSON Resume)">',
        '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False).replace('</', '<\\/'),
    ])

    bio = ''.join([
        "<p>Hi, I'm %s.</p>" % esc(p['firstName']),
        '<p>%s @ %s%s.</p>' % (esc(now['positions'][0]['title']), esc(now['company']),
                               ', ' + esc(now['tagline']) if now.get('tagline') else ''),
        '<p>%s</p>' % esc(data['intro']),
        '<p>Based in %s.</p>' % esc(p['location']),
    ])

    link_row = ' / '.join([
        '<a href="%s" target="_blank" rel="noopener">github</a>' % url['github'],
        '<a href="%s" target="_blank" rel="noopener">linkedin</a>' % url['linkedin'],
        '<a href="mailto:%s" data-copy="%s" title="copy %s">email</a>' % ((esc(p['email']),) * 3),
        '<a href="#resume">resume ↓</a>',
    ])

    jobs = []
    for e in data['experience']:
        roles = []
        for i, r in enumerate(e['positions']):
            items = ''.join('<li>%s</li>' % esc(a) for a in r.get('achievements', []))
            roles.append(
                '<details class="role"%s><summary><span class="role-title">%s</span><span class="date">%s</span></summary>'
                '<ul>%s</ul></details>' % (' open' if e is now and i == 0 else '', esc(r['title']), esc(r['dateRange']), items))
        tag = '<span class="job-tag">%s</span>' % esc(e['tagline']) if e.get('tagline') else ''
        jobs.append('<div class="job"><div class="job-head"><span class="job-co">%s</span>%s</div>%s</div>'
                    % (esc(e['company']), tag, ''.join(roles)))

    skills = ' <i>/</i> '.join('<span>%s</span>' % esc(s)
                               for s in data['skills']['technical'] + data['skills']['leadership'])

    foot = '%s, %s%s · %s — © %d %s · <a href="llms.txt">hi, agents →</a>' % (
        esc(ed['degree']), esc(ed['school']), ' (minor: %s)' % esc(ed['minor']) if ed.get('minor') else '',
        esc(ed['graduationDate']), datetime.date.today().year, esc(name))

    return {'head': head, 'bio': bio, 'links': link_row, 'jobs': '\n'.join(jobs), 'skills': skills, 'foot': foot}


def fill(page, regions):
    for name, content in regions.items():
        pattern = re.compile(r'(<!-- gen:%s -->).*?(<!-- /gen:%s -->)' % (name, name), re.S)
        if not pattern.search(page):
            raise SystemExit('index.html is missing <!-- gen:%s --> markers' % name)
        block = '\n%s\n' % content if '\n' in content else content
        page = pattern.sub(lambda m: m.group(1) + block + m.group(2), page)
    return page


# ---------- files for agents ----------

def resume_md(data):
    p, out = data['personal'], []
    out += ['# %s %s' % (p['firstName'], p['lastName']), '', '**%s** · %s' % (p['title'], p['location']), '',
            '%s · %s · linkedin.com/in/%s · %s' % (p['email'], p['phone'], p['linkedin'], p['websiteUrl']), '',
            strip(data['about']), '', '## Experience', '']
    for e in data['experience']:
        out += ['### %s%s' % (e['company'], ' — ' + strip(e['tagline']) if e.get('tagline') else ''), '']
        for r in e['positions']:
            out += ['**%s** · %s' % (strip(r['title']), r['dateRange']), '']
            out += ['- %s' % strip(a) for a in r.get('achievements', [])]
            out.append('')
    ed = data['education']
    out += ['## Skills', '', '**Technical:** %s' % ', '.join(data['skills']['technical']), '',
            '**Leadership:** %s' % ', '.join(data['skills']['leadership']), '', '## Education', '',
            '%s%s — %s, %s' % (ed['degree'], ', minor in ' + ed['minor'] if ed.get('minor') else '',
                              ed['school'], ed['graduationDate']), '']
    return '\n'.join(out)


def resume_txt(data):
    p, out = data['personal'], []
    rule = lambda s: s.upper() + '\n' + '-' * len(s)
    out += ['%s %s' % (p['firstName'].upper(), p['lastName'].upper()), p['title'],
            '%s | %s | %s' % (p['location'], p['email'], p['phone']),
            'linkedin.com/in/%s | %s' % (p['linkedin'], p['websiteUrl']), '', rule('Summary'), strip(data['about']),
            '', rule('Experience')]
    for e in data['experience']:
        for r in e['positions']:
            out += ['', '%s, %s' % (strip(r['title']), e['company']), r['dateRange']]
            out += ['  * %s' % strip(a) for a in r.get('achievements', [])]
    ed = data['education']
    out += ['', rule('Skills'), ', '.join(data['skills']['technical']), ', '.join(data['skills']['leadership']), '',
            rule('Education'), '%s, %s, %s' % (ed['degree'], ed['school'], ed['graduationDate']), '']
    return '\n'.join(out)


def resume_json(data):
    """The JSON Resume schema (jsonresume.org), which resume parsers and agents already understand"""
    p, url, ed = data['personal'], links(data), data['education']
    city, region = [s.strip() for s in p['location'].split(',')]
    work = []
    for e in data['experience']:
        for r in e['positions']:
            start, end = date_range(r['dateRange'])
            job = {'name': e['company'], 'position': strip(r['title']), 'startDate': start}
            if end:
                job['endDate'] = end
            if e.get('tagline'):
                job['description'] = strip(e['tagline'])
            job['highlights'] = [strip(a) for a in r.get('achievements', [])]
            work.append(job)
    grad = date_range(ed['graduationDate'])[0]
    return json.dumps({
        '$schema': 'https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json',
        'basics': {
            'name': '%s %s' % (p['firstName'], p['lastName']), 'label': p['title'], 'email': p['email'],
            'phone': p['phone'], 'url': url['site'] + '/', 'summary': strip(data['about']),
            'location': {'city': city, 'region': region, 'countryCode': 'US'},
            'profiles': [{'network': 'LinkedIn', 'username': p['linkedin'], 'url': url['linkedin']},
                         {'network': 'GitHub', 'username': p['github'], 'url': url['github']}],
        },
        'work': work,
        'education': [{'institution': ed['school'], 'area': ed['degree'].replace('BS ', ''), 'studyType': 'Bachelor of Science',
                       'endDate': grad}],
        'skills': [{'name': 'Technical', 'keywords': data['skills']['technical']},
                   {'name': 'Leadership', 'keywords': data['skills']['leadership']}],
        'meta': {'canonical': url['site'] + '/resume.json', 'note': strip(data['agentNote'])},
    }, indent=2, ensure_ascii=False) + '\n'


def llms_txt(data):
    """llms.txt (llmstxt.org): the page an AI agent should read first"""
    p, url, ed = data['personal'], links(data), data['education']
    name = '%s %s' % (p['firstName'], p['lastName'])
    now = data['experience'][0]
    out = ['# %s' % name, '',
           '> %s at %s, based in %s. %s' % (p['title'], now['company'], p['location'], strip(data['intro'])), '',
           strip(data['about']), '', '## Hello, agent', '', strip(data['agentNote']), '',
           '- Email: %s' % p['email'], '- LinkedIn: %s' % url['linkedin'], '- GitHub: %s' % url['github'],
           '- Website: %s/' % url['site'], '', '## Experience', '']
    for e in data['experience']:
        for r in e['positions']:
            out.append('### %s, %s (%s)' % (strip(r['title']), e['company'], r['dateRange']))
            out.append('')
            out += ['- %s' % strip(a) for a in r.get('achievements', [])]
            out.append('')
    out += ['## Skills', '', ', '.join(data['skills']['technical'] + data['skills']['leadership']), '',
            '## Education', '', '%s, %s%s, %s' % (ed['degree'], ed['school'],
                                                  ' (minor: %s)' % ed['minor'] if ed.get('minor') else '', ed['graduationDate']), '',
            '## Resume', '',
            '- [Resume (PDF)](%s/resume.pdf): the one-page version' % url['site'],
            '- [Resume (Markdown)](%s/resume.md): same content, easy to read' % url['site'],
            '- [Resume (JSON Resume)](%s/resume.json): structured, jsonresume.org schema' % url['site'],
            '- [Resume (plain text)](%s/resume.txt): for ATS and parsers' % url['site'], '']
    return '\n'.join(out)


def robots_txt(data):
    site = links(data)['site']
    return 'User-agent: *\nAllow: /\n\n# AI crawlers and agents are welcome. Start with /llms.txt.\n%s\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % (
        '\n'.join('User-agent: %s' % b for b in AI_CRAWLERS), site)


def sitemap_xml(data):
    site = links(data)['site']
    urls = ['/', '/llms.txt', '/resume.md', '/resume.json', '/resume.pdf']
    body = ''.join('  <url><loc>%s%s</loc></url>\n' % (site, u) for u in urls)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % body


def main():
    data = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))
    index = ROOT / 'index.html'
    index.write_text(fill(index.read_text(encoding='utf-8'), html_regions(data)), encoding='utf-8')
    files = {
        'llms.txt': llms_txt(data), 'resume.md': resume_md(data), 'resume.txt': resume_txt(data),
        'resume.json': resume_json(data), 'robots.txt': robots_txt(data), 'sitemap.xml': sitemap_xml(data),
    }
    for name, text in files.items():
        (ROOT / name).write_text(text, encoding='utf-8')
    print('✓ Generated index.html content, %s' % ', '.join(files))


if __name__ == '__main__':
    main()
