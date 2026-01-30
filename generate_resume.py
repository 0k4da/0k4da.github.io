#!/usr/bin/env python3
"""
Generate LaTeX resume from data.json with multiple template options

Usage:
    python generate_resume.py                  # Uses default (original) template
    python generate_resume.py --template original
    python generate_resume.py --template classic
    python generate_resume.py --template modern
    python generate_resume.py --list           # List available templates
"""

import json
import argparse
import qrcode


def escape_latex(text):
    """Escape special LaTeX characters"""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def generate_qr_code(url, filename='qr_code.png'):
    """Generate QR code for given URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"  Generated QR code: {filename}")


# =============================================================================
# TEMPLATE: ORIGINAL (Two-column with light sidebar, copper accents)
# =============================================================================
def generate_original_template(data):
    """Original template - Two-column with light sidebar and copper accents"""

    latex = r"""\documentclass[10pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0pt]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{graphicx}

% Sophisticated color palette
\definecolor{primary}{RGB}{0,0,0}
\definecolor{accent}{RGB}{204,147,100}
\definecolor{sidebarBg}{RGB}{245,250,250}
\definecolor{darkgray}{RGB}{40,40,40}
\definecolor{mediumgray}{RGB}{100,100,100}
\definecolor{lightgray}{RGB}{240,240,240}
\definecolor{company1}{RGB}{70,130,180}
\definecolor{company2}{RGB}{100,149,237}
\definecolor{company3}{RGB}{205,92,92}

% Modern fonts (TeX Gyre Heros is a Helvetica clone)
\setmainfont{TeX Gyre Heros}
\newfontfamily\displayfont[LetterSpace=15.0]{TeX Gyre Heros}
\newfontfamily\headingfont{TeX Gyre Heros}

% Eliminate spacing
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\pagenumbering{gobble}
\pagestyle{empty}

% Custom commands
\newcommand{\sidebarheader}[1]{%
    \vspace{6pt}
    {\headingfont\small\textcolor{accent}{\MakeUppercase{\textbf{#1}}}}
    \vspace{1pt}
    \par\noindent\textcolor{accent}{\rule{\linewidth}{1.5pt}}
    \vspace{2pt}
}

\newcommand{\mainheader}[1]{%
    \vspace{6pt}
    {\displayfont\Large\textcolor{accent}{\MakeUppercase{#1}}}
    \vspace{1pt}
    \par\noindent\textcolor{accent}{\rule{5.0in}{2pt}}
    \vspace{3pt}
}

\newcommand{\companyHeader}[2]{%
    \vspace{3pt}
    \noindent\textcolor{#2}{\rule{3pt}{10pt}}\hspace{6pt}{\headingfont\normalsize\textbf{\textcolor{darkgray}{#1}}}
    \vspace{1pt}
}

\newcommand{\positionHeader}[2]{%
    \noindent\textbf{\textcolor{darkgray}{#2}}\hspace{4pt}{\footnotesize\textcolor{mediumgray}{//}}\hspace{4pt}{\footnotesize\itshape\textcolor{mediumgray}{#1}}
    \vspace{1pt}
}

% Minimalist bullets
\renewcommand{\labelitemi}{\textcolor{accent}{—}}
\setlength{\leftmargini}{10pt}

\begin{document}

% LEFT SIDEBAR WITH BACKGROUND COLOR
\setlength{\voffset}{-.085in}
\noindent\colorbox{sidebarBg}{%
\begin{minipage}[t][10.885in][t]{2.7in}
\vspace{0.3in}
\hspace{0.3in}
\begin{minipage}{2.1in}
\raggedright

"""

    # Personal info
    personal = data['personal']
    latex += f"""% IDENTITY
{{\\displayfont\\fontsize{{24}}{{28}}\\selectfont\\textcolor{{primary}}{{\\textbf{{{personal['firstName'].upper()}}}}}}}\\\\[-2pt]
{{\\displayfont\\fontsize{{24}}{{28}}\\selectfont\\textcolor{{accent}}{{\\textbf{{{personal['lastName'].upper()}}}}}}}

\\vspace{{4pt}}
\\noindent\\textcolor{{accent}}{{\\rule{{1.8in}}{{2.5pt}}}}
\\vspace{{6pt}}

{{\\headingfont\\small\\textcolor{{darkgray}}{{\\textbf{{{personal['title']}}}}}}}

\\vspace{{6pt}}

{{\\footnotesize\\textcolor{{mediumgray}}{{\\\\[-6pt]
{personal['phone']}\\\\[3pt]
{personal['email']}\\\\[3pt]
@{personal['linkedin']}\\\\[3pt]
{personal['location']}\\\\[3pt]
}}}}

"""

    # About section
    latex += f"""% ABOUT
\\sidebarheader{{About}}
{{\\footnotesize\\textcolor{{darkgray}}{{\\\\[-6pt]\\itshape {escape_latex(data['about'])}}}}}

"""

    # Technical skills
    latex += """% TECHNICAL FOUNDATION
\\sidebarheader{Technical Foundation}
{\\scriptsize\\textcolor{darkgray}{\\\\[-6pt]
"""
    for skill in data['skills']['technical']:
        latex += f"{escape_latex(skill)}\\\\[3pt]\n"
    latex += "}}\n\n"

    # Leadership skills
    latex += """% LEADERSHIP
\\sidebarheader{Leadership}
{\\scriptsize\\textcolor{darkgray}{\\\\[-6pt]
"""
    for skill in data['skills']['leadership']:
        latex += f"{escape_latex(skill)}\\\\[3pt]\n"
    latex += "}}\n\n"

    # Education
    edu = data['education']
    latex += f"""% EDUCATION
\\sidebarheader{{Education}}
{{\\footnotesize\\\\[-6pt]
\\textbf{{\\textcolor{{darkgray}}{{{edu['school']}}}}}\\\\[3pt]
\\textcolor{{mediumgray}}{{{edu['graduationDate']}}}\\\\[3pt]
\\textcolor{{darkgray}}{{Major: {edu['degree'].replace('BS ', '')}\\\\[3pt]
Minor: {edu['minor']}\\\\[3pt]}}
}}

\\vfill

% QR CODE
\\vspace{{80pt}}
\\raggedright
\\includegraphics[width=0.8in]{{qr_code.png}}\\\\[3pt]

\\vspace{{10pt}}

"""

    # Close sidebar
    latex += r"""\end{minipage}
\end{minipage}%
}%
% RIGHT MAIN CONTENT
\hspace{0pt}%
\begin{minipage}[t][10.5in][t]{5.6in}
\vspace{0.3in}
\hspace{0.3in}
\begin{minipage}{5.0in}
\raggedright

% EXPERIENCE
\mainheader{Experience}
\vspace{-8pt}

"""

    # Experience section
    for company_data in data['experience']:
        company = company_data['company']
        color = company_data['color']

        latex += f"\\companyHeader{{{escape_latex(company)}}}{{{color}}}\n\n"

        for position in company_data['positions']:
            latex += f"\\positionHeader{{{position['dateRange']}}}{{{escape_latex(position['title'])}}}\n"
            latex += "\\begin{itemize}\n"
            latex += "    \\setlength\\itemsep{0.25pt}\n"

            for achievement in position['achievements']:
                latex += f"    \\item\\small\\textcolor{{darkgray}}{{{escape_latex(achievement)}}}\n"

            latex += "\\end{itemize}\n\n"

            if position != company_data['positions'][-1]:
                latex += "\\vspace{1pt}\n\n"

    latex += r"""\end{minipage}
\end{minipage}

\end{document}
"""

    return latex


# =============================================================================
# TEMPLATE: CLASSIC (Single-column, traditional, ATS-friendly)
# =============================================================================
def generate_classic_template(data):
    """Classic template - Traditional single-column, clean and ATS-friendly"""

    latex = r"""\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[top=0.5in, bottom=0.5in, left=0.6in, right=0.6in]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{hyperref}

% Classic color palette - professional blues
\definecolor{primary}{RGB}{30,60,90}
\definecolor{accent}{RGB}{51,102,153}
\definecolor{darktext}{RGB}{33,33,33}
\definecolor{mediumtext}{RGB}{85,85,85}
\definecolor{lighttext}{RGB}{120,120,120}
\definecolor{rulecolor}{RGB}{51,102,153}

% Clean fonts (TeX Gyre Heros is a Helvetica clone)
\setmainfont{TeX Gyre Heros}
\newfontfamily\headingfont[BoldFont={TeX Gyre Heros Bold}]{TeX Gyre Heros}

% Spacing
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\pagenumbering{gobble}

% Section formatting
\titleformat{\section}
    {\headingfont\large\color{primary}\MakeUppercase}
    {}
    {0pt}
    {}
    [\vspace{-6pt}\textcolor{rulecolor}{\rule{\textwidth}{1.5pt}}\vspace{4pt}]

\titlespacing*{\section}{0pt}{14pt}{8pt}

% Hyperlinks
\hypersetup{
    colorlinks=true,
    linkcolor=accent,
    urlcolor=accent
}

% List settings
\setlist[itemize]{leftmargin=15pt, itemsep=2pt, parsep=0pt, topsep=4pt}
\renewcommand{\labelitemi}{\textcolor{accent}{\textbullet}}

\begin{document}

"""

    personal = data['personal']

    # Header
    latex += f"""% HEADER
\\begin{{center}}
{{\\headingfont\\fontsize{{26}}{{30}}\\selectfont\\textcolor{{primary}}{{{personal['firstName']} {personal['lastName']}}}}}

\\vspace{{6pt}}

{{\\large\\textcolor{{accent}}{{{personal['title']}}}}}

\\vspace{{8pt}}

{{\\small\\textcolor{{mediumtext}}{{
{personal['phone']} \\hspace{{8pt}} | \\hspace{{8pt}}
\\href{{mailto:{personal['email']}}}{{{personal['email']}}} \\hspace{{8pt}} | \\hspace{{8pt}}
\\href{{https://linkedin.com/in/{personal['linkedin']}}}{{linkedin.com/in/{personal['linkedin']}}} \\hspace{{8pt}} | \\hspace{{8pt}}
{personal['location']}
}}}}
\\end{{center}}

\\vspace{{4pt}}

"""

    # Summary
    latex += f"""% SUMMARY
\\section{{Summary}}
{{\\textcolor{{darktext}}{{{escape_latex(data['about'])}}}}}

"""

    # Experience
    latex += """% EXPERIENCE
\\section{Experience}

"""

    for company_data in data['experience']:
        company = company_data['company']

        for position in company_data['positions']:
            latex += f"""\\noindent\\textbf{{\\textcolor{{primary}}{{{escape_latex(company)}}}}} \\hfill \\textcolor{{lighttext}}{{{position['dateRange']}}}\\\\
\\textit{{\\textcolor{{accent}}{{{escape_latex(position['title'])}}}}}
\\begin{{itemize}}
"""
            for achievement in position['achievements']:
                latex += f"    \\item\\small\\textcolor{{darktext}}{{{escape_latex(achievement)}}}\n"

            latex += "\\end{itemize}\n\\vspace{6pt}\n\n"

    # Skills
    latex += """% SKILLS
\\section{Skills}

\\vspace{2pt}

"""

    latex += f"""\\noindent\\textbf{{\\textcolor{{primary}}{{Technical:}}}} \\textcolor{{darktext}}{{{', '.join([escape_latex(s) for s in data['skills']['technical']])}}}

\\vspace{{6pt}}

\\noindent\\textbf{{\\textcolor{{primary}}{{Leadership:}}}} \\textcolor{{darktext}}{{{', '.join([escape_latex(s) for s in data['skills']['leadership']])}}}

"""

    # Education
    edu = data['education']
    latex += f"""% EDUCATION
\\section{{Education}}

\\noindent\\textbf{{\\textcolor{{primary}}{{{edu['school']}}}}} \\hfill \\textcolor{{lighttext}}{{{edu['graduationDate']}}}\\\\
\\textcolor{{darktext}}{{{edu['degree']}, Minor: {edu['minor']}}}

\\end{{document}}
"""

    return latex


# =============================================================================
# TEMPLATE: MODERN (Dark header, bold design, vibrant accents)
# =============================================================================
def generate_modern_template(data):
    """Modern template - Dark header with bold design and vibrant accents"""

    latex = r"""\documentclass[10pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0pt]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{enumitem}

% Modern vibrant palette
\definecolor{headerBg}{RGB}{20,25,45}
\definecolor{accentCyan}{RGB}{0,200,220}
\definecolor{accentGreen}{RGB}{0,220,130}
\definecolor{darktext}{RGB}{45,45,55}
\definecolor{mediumtext}{RGB}{90,90,100}
\definecolor{lightBg}{RGB}{250,251,252}
\definecolor{cardBg}{RGB}{255,255,255}
\definecolor{company1}{RGB}{0,180,200}
\definecolor{company2}{RGB}{0,200,130}
\definecolor{company3}{RGB}{150,100,200}

% Modern fonts (TeX Gyre Heros is a Helvetica clone)
\setmainfont{TeX Gyre Heros}
\newfontfamily\displayfont[LetterSpace=12.0]{TeX Gyre Heros}
\newfontfamily\headingfont[BoldFont={TeX Gyre Heros Bold}]{TeX Gyre Heros}

% Spacing
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\pagenumbering{gobble}
\pagestyle{empty}

% Custom commands
\newcommand{\sectiontitle}[1]{%
    \vspace{10pt}
    {\displayfont\normalsize\textcolor{headerBg}{\MakeUppercase{\textbf{#1}}}}
    \vspace{2pt}
    \par\noindent\textcolor{accentCyan}{\rule{1.2in}{2.5pt}}
    \vspace{6pt}
}

\newcommand{\companyBlock}[3]{%
    \vspace{4pt}
    \noindent\colorbox{#3}{\textcolor{white}{\scriptsize\textbf{\hspace{3pt}#1\hspace{3pt}}}}
    \vspace{2pt}
}

% List settings
\setlist[itemize]{leftmargin=12pt, itemsep=1pt, parsep=0pt, topsep=3pt}

\begin{document}

"""

    personal = data['personal']

    # Dark Header
    latex += f"""% DARK HEADER
\\noindent\\colorbox{{headerBg}}{{%
\\begin{{minipage}}[t][2.2in][t]{{\\paperwidth}}
\\vspace{{0.4in}}
\\hspace{{0.5in}}
\\begin{{minipage}}{{7in}}

% Name
{{\\displayfont\\fontsize{{32}}{{36}}\\selectfont\\textcolor{{white}}{{\\textbf{{{personal['firstName'].upper()} {personal['lastName'].upper()}}}}}}}

\\vspace{{8pt}}

% Title with accent
{{\\large\\textcolor{{accentCyan}}{{{personal['title'].upper()}}}}}

\\vspace{{16pt}}

% Contact row
{{\\small\\textcolor{{white}}{{
{personal['phone']} \\hspace{{15pt}}
{personal['email']} \\hspace{{15pt}}
@{personal['linkedin']} \\hspace{{15pt}}
{personal['location']}
}}}}

\\end{{minipage}}
\\end{{minipage}}%
}}

"""

    # Main content
    latex += r"""% MAIN CONTENT
\noindent\colorbox{lightBg}{%
\begin{minipage}[t][8.6in][t]{\paperwidth}
\vspace{0.3in}
\hspace{0.5in}
\begin{minipage}[t]{3.2in}
\raggedright

"""

    # Left column - About & Skills
    latex += f"""% ABOUT
\\sectiontitle{{About}}
{{\\small\\textcolor{{darktext}}{{{escape_latex(data['about'])}}}}}

% SKILLS
\\sectiontitle{{Technical Skills}}
{{\\scriptsize\\textcolor{{mediumtext}}{{
"""

    for skill in data['skills']['technical']:
        latex += f"\\textcolor{{accentCyan}}{{\\textbullet}} {escape_latex(skill)}\\\\[4pt]\n"

    latex += "}}\n\n"

    latex += """\\sectiontitle{Leadership}
{\\scriptsize\\textcolor{mediumtext}{
"""

    for skill in data['skills']['leadership']:
        latex += f"\\textcolor{{accentGreen}}{{\\textbullet}} {escape_latex(skill)}\\\\[4pt]\n"

    latex += "}}\n\n"

    # Education
    edu = data['education']
    latex += f"""% EDUCATION
\\sectiontitle{{Education}}
{{\\small
\\textbf{{\\textcolor{{darktext}}{{{edu['school']}}}}}\\\\[3pt]
\\textcolor{{mediumtext}}{{{edu['degree']}}}\\\\[2pt]
\\textcolor{{mediumtext}}{{Minor: {edu['minor']}}}\\\\[2pt]
\\textcolor{{accentCyan}}{{{edu['graduationDate']}}}
}}

"""

    # Close left column, start right column
    latex += r"""\end{minipage}%
\hspace{0.3in}%
\begin{minipage}[t]{4in}
\raggedright

% EXPERIENCE
\sectiontitle{Experience}

"""

    # Experience
    color_map = {
        'company1': 'company1',
        'company2': 'company2',
        'company3': 'company3'
    }

    for company_data in data['experience']:
        company = company_data['company']
        color = color_map.get(company_data['color'], 'accentCyan')

        for position in company_data['positions']:
            latex += f"""\\companyBlock{{{escape_latex(company)}}}{{{position['dateRange']}}}{{{color}}}

\\noindent{{\\small\\textbf{{\\textcolor{{darktext}}{{{escape_latex(position['title'])}}}}}}} \\hfill {{\\scriptsize\\textcolor{{mediumtext}}{{{position['dateRange']}}}}}
\\begin{{itemize}}
\\renewcommand{{\\labelitemi}}{{\\textcolor{{{color}}}{{\\rule{{4pt}}{{4pt}}}}}}
"""

            for achievement in position['achievements']:
                latex += f"    \\item{{\\scriptsize\\textcolor{{darktext}}{{{escape_latex(achievement)}}}}}\n"

            latex += "\\end{itemize}\n\\vspace{4pt}\n\n"

    # Close document
    latex += r"""\end{minipage}
\end{minipage}%
}

\end{document}
"""

    return latex


# =============================================================================
# TEMPLATE REGISTRY
# =============================================================================
TEMPLATES = {
    'original': {
        'name': 'Original',
        'description': 'Two-column with light sidebar and copper accents',
        'generator': generate_original_template,
    },
    'classic': {
        'name': 'Classic',
        'description': 'Traditional single-column, clean and ATS-friendly',
        'generator': generate_classic_template,
    },
    'modern': {
        'name': 'Modern',
        'description': 'Dark header with bold design and vibrant cyan/green accents',
        'generator': generate_modern_template,
    },
}


def list_templates():
    """Print available templates"""
    print("\nAvailable Resume Templates:")
    print("-" * 50)
    for key, template in TEMPLATES.items():
        print(f"  {key:12} - {template['name']}")
        print(f"               {template['description']}")
        print()


def main():
    import subprocess

    parser = argparse.ArgumentParser(
        description='Generate LaTeX resume from data.json',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_resume.py                    # Uses original template
  python generate_resume.py --template classic # Uses classic template
  python generate_resume.py --template modern  # Uses modern template
  python generate_resume.py --list             # List all templates
        """
    )
    parser.add_argument(
        '--template', '-t',
        choices=list(TEMPLATES.keys()),
        default='original',
        help='Template style to use (default: original)'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available templates and exit'
    )
    parser.add_argument(
        '--output', '-o',
        default='resume',
        help='Output filename without extension (default: resume)'
    )

    args = parser.parse_args()

    if args.list:
        list_templates()
        return

    # Load data from JSON
    with open('data.json', 'r') as f:
        data = json.load(f)

    template_info = TEMPLATES[args.template]
    print(f"\nGenerating resume with '{template_info['name']}' template...")

    # Generate QR code for website (only for templates that use it)
    if args.template == 'original' and 'websiteUrl' in data['personal']:
        generate_qr_code(data['personal']['websiteUrl'], 'qr_code.png')

    # Generate LaTeX using selected template
    latex_content = template_info['generator'](data)

    # Write to file
    tex_file = f"{args.output}.tex"
    with open(tex_file, 'w') as f:
        f.write(latex_content)

    print(f"  Generated {tex_file}")

    # Build PDF
    print("  Building PDF...")
    try:
        result = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', tex_file],
            capture_output=True,
            text=True,
            check=False
        )

        # Clean up auxiliary files
        import os
        for ext in ['.aux', '.log', '.out']:
            aux_file = f"{args.output}{ext}"
            if os.path.exists(aux_file):
                os.remove(aux_file)

        pdf_file = f"{args.output}.pdf"
        if os.path.exists(pdf_file):
            print(f"  Successfully built: {pdf_file}")
        else:
            print(f"  Build failed. Check {tex_file} for errors.")
            if result.stderr:
                print(result.stderr[:500])
    except FileNotFoundError:
        print("  Warning: xelatex not found. LaTeX file generated but PDF not built.")
        print(f"  Run 'xelatex {tex_file}' manually to generate PDF.")


if __name__ == '__main__':
    main()
