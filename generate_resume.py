#!/usr/bin/env python3
"""
Generate LaTeX resume from data.json
"""

import json
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
    print(f"✓ Generated QR code: {filename}")


def generate_latex_resume(data):
    """Generate LaTeX resume from JSON data"""

    # Start with document preamble
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

% Modern fonts
\setmainfont{Helvetica Neue}
\newfontfamily\displayfont[LetterSpace=15.0]{Helvetica Neue}
\newfontfamily\headingfont{Helvetica Neue}

% Eliminate spacing
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\pagenumbering{gobble}
\pagestyle{empty}

% Custom commands
\newcommand{\sidebarheader}[1]{%
    \vspace{8pt}
    {\headingfont\small\textcolor{accent}{\MakeUppercase{\textbf{#1}}}}
    \vspace{2pt}
    \par\noindent\textcolor{accent}{\rule{\linewidth}{1.5pt}}
    \vspace{3pt}
}

\newcommand{\mainheader}[1]{%
    \vspace{8pt}
    {\displayfont\Large\textcolor{accent}{\MakeUppercase{#1}}}
    \vspace{2pt}
    \par\noindent\textcolor{accent}{\rule{4.7in}{2pt}}
    \vspace{5pt}
}

\newcommand{\companyHeader}[2]{%
    \vspace{5pt}
    \noindent\textcolor{#2}{\rule{3pt}{10pt}}\hspace{6pt}{\headingfont\normalsize\textbf{\textcolor{darkgray}{#1}}}
    \vspace{2pt}
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
\noindent\colorbox{sidebarBg}{%
\begin{minipage}[t][10.5in][t]{2.7in}
\vspace{0.4in}
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
@{personal['github']}\\\\[3pt]
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

\\vspace{{10pt}}

% QR CODE
\\begin{{center}}
\\includegraphics[width=0.8in]{{qr_code.png}}\\\\[3pt]
{{\\tiny\\textcolor{{mediumgray}}{{Scan for portfolio}}}}
\\end{{center}}

"""

    # Close sidebar
    latex += r"""\end{minipage}
\end{minipage}%
}%
% RIGHT MAIN CONTENT
\hspace{0pt}%
\begin{minipage}[t][10.5in][t]{5.3in}
\vspace{0.4in}
\hspace{0.3in}
\begin{minipage}{4.7in}
\raggedright

% EXPERIENCE
\mainheader{Experience}

"""

    # Experience section
    for company_data in data['experience']:
        company = company_data['company']
        color = company_data['color']

        # Add company header for first position
        latex += f"\\companyHeader{{{escape_latex(company)}}}{{{color}}}\n\n"

        for position in company_data['positions']:
            latex += f"\\positionHeader{{{position['dateRange']}}}{{{escape_latex(position['title'])}}}\n"
            latex += "\\begin{itemize}\n"
            latex += "    \\setlength\\itemsep{1pt}\n"

            for achievement in position['achievements']:
                latex += f"    \\item\\small\\textcolor{{darkgray}}{{{escape_latex(achievement)}}}\n"

            latex += "\\end{itemize}\n\n"

            # Add spacing between positions except the last one
            if position != company_data['positions'][-1]:
                latex += "\\vspace{2pt}\n\n"

    # Close document
    latex += r"""\end{minipage}
\end{minipage}

\end{document}
"""

    return latex


def main():
    # Load data from JSON
    with open('data.json', 'r') as f:
        data = json.load(f)

    # Generate QR code for website
    if 'websiteUrl' in data['personal']:
        generate_qr_code(data['personal']['websiteUrl'], 'qr_code.png')

    # Generate LaTeX
    latex_content = generate_latex_resume(data)

    # Write to file
    with open('resume.tex', 'w') as f:
        f.write(latex_content)

    print("✓ Generated resume.tex from data.json")


if __name__ == '__main__':
    main()
