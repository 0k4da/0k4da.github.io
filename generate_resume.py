#!/usr/bin/env python3
"""
Generate resume.tex from data.json.

Styling lives in resume.cls; this script only emits content. Standard library
only. Run ./build.sh to generate and compile in one step.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LATEX_ESCAPES = {
    '\\': r'\textbackslash{}',
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
}


def escape_latex(text):
    """Escape special LaTeX characters (single pass, so escapes aren't re-escaped)"""
    return ''.join(LATEX_ESCAPES.get(ch, ch) for ch in str(text))


def generate_latex_resume(data):
    """Generate LaTeX resume content from JSON data"""
    e = escape_latex
    personal = data['personal']
    lines = [
        r'\documentclass{resume}',
        r'\hypersetup{pdftitle={%s %s - Resume}, pdfauthor={%s %s}}' % (
            e(personal['firstName']), e(personal['lastName']),
            e(personal['firstName']), e(personal['lastName'])),
        r'\begin{document}',
        '',
        r'\begin{sidebar}',
        r'\name{%s}{%s}' % (e(personal['firstName']), e(personal['lastName'])),
        r'\jobtitle{%s}' % e(personal['title']),
        r'\contact{T}{tel:%s}{%s}' % (
            ''.join(ch for ch in personal['phone'] if ch.isdigit()), e(personal['phone'])),
        r'\contact{E}{mailto:%s}{%s}' % (personal['email'], e(personal['email'])),
        r'\contact{in}{https://linkedin.com/in/%s}{%s}' % (
            personal['linkedin'], e(personal['linkedin'])),
        r'\contact{L}{}{%s}' % e(personal['location']),
        '',
        r'\sidebarsection{About}',
        r'\aboutblurb{%s}' % e(data['about']),
        '',
        r'\sidebarsection{Technical Foundation}',
        *(r'\skill{%s}' % e(skill) for skill in data['skills']['technical']),
        '',
        r'\sidebarsection{Leadership}',
        *(r'\skill{%s}' % e(skill) for skill in data['skills']['leadership']),
        '',
    ]

    edu = data['education']
    lines += [
        r'\sidebarsection{Education}',
        r'\sidebartext{\textbf{%s}\\%s\\Minor in %s\\{\color{mediumgray}%s}}' % (
            e(edu['school']), e(edu['degree']), e(edu['minor']), e(edu['graduationDate'])),
        '',
    ]

    if 'websiteUrl' in personal:
        url = personal['websiteUrl']
        lines.append(r'\websiteqr{%s}{%s}' % (url, e(url.split('://', 1)[-1])))

    lines += [r'\end{sidebar}%', r'\begin{maincolumn}', r'\mainsection{Experience}', '']

    for company in data['experience']:
        lines.append(r'\company{%s}{%s}{%s}' % (
            e(company['company']), company['color'], e(company.get('tagline', ''))))
        for position in company['positions']:
            lines.append(r'\position{%s}{%s}' % (e(position['title']), e(position['dateRange'])))
            lines.append(r'\begin{itemize}')
            lines += [r'    \achievement{%s}' % e(a) for a in position['achievements']]
            lines.append(r'\end{itemize}')
        lines.append('')

    lines += [r'\end{maincolumn}', r'\end{document}', '']
    return '\n'.join(lines)


def main():
    data = json.loads((ROOT / 'data.json').read_text())
    (ROOT / 'resume.tex').write_text(generate_latex_resume(data))
    print('✓ Generated resume.tex from data.json')


if __name__ == '__main__':
    sys.exit(main())
