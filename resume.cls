% resume.cls — layout and typography for resume.tex
% Content is generated from data.json by generate_resume.py; edit styling here.
%
% Type: Didot (name, companies) · Avenir Next (text) · Menlo (technical labels)
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2026/10/26 Two-column resume]

\LoadClass[10pt,letterpaper]{article}

\RequirePackage[letterpaper,top=0.42in,bottom=0.32in,left=0.42in,right=0.45in]{geometry}
\RequirePackage{fontspec}
\RequirePackage{xcolor}
\RequirePackage{tikz}
\RequirePackage{eso-pic}
\RequirePackage{enumitem}
\RequirePackage{qrcode}
\RequirePackage{microtype}
\RequirePackage[hidelinks]{hyperref}

% ---------------------------------------------------------------- Colors
\definecolor{ink}{HTML}{1C1B1A}
\definecolor{accent}{HTML}{A8673A}
\definecolor{paper}{HTML}{F7F5F1}
\definecolor{gridgray}{HTML}{DDD7CE}
\definecolor{rulegray}{HTML}{D8D2C9}
\definecolor{darkgray}{HTML}{2E2C2A}
\definecolor{mediumgray}{HTML}{77716A}
% Company colors are kept for the website; the PDF uses the single accent
\definecolor{company1}{HTML}{4682B4}
\definecolor{company2}{HTML}{6495ED}
\definecolor{company3}{HTML}{CD5C5C}
\definecolor{company4}{HTML}{3D9A8B}

% ---------------------------------------------------------------- Fonts
\setmainfont{Avenir Next}[
    UprightFont = {Avenir Next Regular},
    BoldFont = {Avenir Next Demi Bold},
    ItalicFont = {Avenir Next Italic},
    BoldItalicFont = {Avenir Next Demi Bold Italic},
]
\newfontfamily\displayfont{Didot}[ItalicFont = {Didot Italic}]
\newfontfamily\techfont{Menlo}[LetterSpace=6.0, Scale=0.92]

% ---------------------------------------------------------------- Page
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlength{\topskip}{0pt}
\pagestyle{empty}
\raggedright

\newlength{\sidebarbg}\setlength{\sidebarbg}{2.62in}
\newlength{\sidebarwidth}\setlength{\sidebarwidth}{1.98in}
\newlength{\maingutter}\setlength{\maingutter}{0.38in}
% x-position of the experience timeline, measured from the page's left edge
\newlength{\timelinex}\setlength{\timelinex}{\dimexpr\sidebarbg+\maingutter-10pt\relax}

% Background: white page, paper-toned sidebar with a faint dot grid, timeline hairline
\AddToShipoutPictureBG{%
    \begin{tikzpicture}[remember picture, overlay]
        \fill[white] (current page.south west) rectangle (current page.north east);
        \fill[paper] (current page.south west) rectangle
            ([xshift=\sidebarbg]current page.north west);
        \foreach \x in {1,...,18} \foreach \y in {1,...,78}
            \fill[gridgray] ([xshift=\x*10pt-1pt, yshift=\y*10pt]current page.south west) circle (0.35pt);
        \draw[rulegray, line width=0.4pt]
            ([xshift=\timelinex, yshift=-0.42in-24pt]current page.north west) --
            ([xshift=\timelinex, yshift=0.5in]current page.south west);
    \end{tikzpicture}%
}

% Columns open with \vspace{0pt} so both align to their top edge rather than first baseline.
% Sidebar spans the full text height so \websiteqr can pin itself to the bottom
\newenvironment{sidebar}
    {\noindent\begin{minipage}[t][\textheight][t]{\sidebarwidth}\vspace{0pt}\raggedright\color{darkgray}}
    {\end{minipage}}

% Main column starts one gutter past the sidebar panel and runs to the right margin
\newenvironment{maincolumn}
    {\hspace{\dimexpr\sidebarbg-0.42in-\sidebarwidth+\maingutter\relax}%
     \begin{minipage}[t]{\dimexpr\textwidth-\sidebarbg+0.42in-\maingutter\relax}\vspace{0pt}\raggedright\color{darkgray}}
    {\end{minipage}}

% ---------------------------------------------------------------- Identity
\newcommand{\name}[2]{%
    {\displayfont\fontsize{31}{30}\selectfont\color{ink}#1\par}
    {\displayfont\itshape\fontsize{31}{32}\selectfont\color{accent}#2\par}
    \vspace{9pt}%
    {\color{accent}\hrule width 0.45in height 0.5pt}%
    \vspace{9pt}%
}

\newcommand{\jobtitle}[1]{{\techfont\scriptsize\color{ink}\MakeUppercase{#1}\par}\vspace{10pt}}

\newcommand{\contact}[3]{% label, url, text
    {\footnotesize\color{darkgray}%
     \makebox[1.6em][l]{\techfont\tiny\color{accent}#1}%
     \if\relax\detokenize{#2}\relax#3\else\href{#2}{#3}\fi\par}\vspace{2.5pt}%
}

% ---------------------------------------------------------------- Sections
% Monospace label followed by a hairline running to the column edge
\newcommand{\sectionlabel}[1]{%
    {\techfont\scriptsize\color{accent}\MakeUppercase{#1}}%
    \hspace{6pt}{\color{rulegray}\leaders\hrule height 2.6pt depth -2.2pt\hfill}\par
}

\newcommand{\sidebarsection}[1]{\vspace{16pt}\sectionlabel{#1}\vspace{8pt}}
\newcommand{\mainsection}[1]{\sectionlabel{#1}\vspace{2pt}}

\newcommand{\sidebartext}[1]{{\footnotesize\color{darkgray}\linespread{1.12}\selectfont #1\par}}
\newcommand{\aboutblurb}[1]{{\fontsize{8.6}{12.4}\selectfont\color{darkgray}#1\par}}
\newcommand{\skill}[1]{{\footnotesize\color{darkgray}#1\par}\vspace{4.5pt}}

% ---------------------------------------------------------------- Experience
% \company{name}{color (unused in PDF)}{tagline, may be empty}
% A ring marker sits on the timeline hairline to the left of the column.
\newcommand{\company}[3]{%
    \vspace{9.5pt}%
    \leavevmode\llap{\makebox[20pt][c]{\tikz[baseline=-2.6pt]\draw[accent, line width=0.7pt, fill=white] (0,0) circle (2.4pt);}}%
    {\displayfont\fontsize{15}{16}\selectfont\color{ink}#1}%
    \if\relax\detokenize{#3}\relax\else
        \hspace{7pt}{\footnotesize\itshape\color{mediumgray}#3}%
    \fi\par\vspace{2pt}%
}

% \position{title}{date range}
\newcommand{\position}[2]{%
    \vspace{3.5pt}%
    {\small\bfseries\color{ink}#1\hfill{\techfont\scriptsize\mdseries\color{mediumgray}#2}\par}
    \vspace{1.5pt}%
}

\setlist[itemize]{
    leftmargin=10pt, labelsep=5pt, topsep=1pt, itemsep=1.8pt, parsep=0pt, partopsep=0pt,
    before={\fontsize{8.8}{11.4}\selectfont\color{darkgray}},
    label={\color{accent}\rule[0.6ex]{4pt}{0.5pt}}
}
\newcommand{\achievement}[1]{\item #1}

% ---------------------------------------------------------------- Footer
% \websiteqr{url}{display text}
\newcommand{\websiteqr}[2]{%
    \vfill
    {\color{ink}\qrcode[height=0.58in,nolink]{#1}\par}\vspace{5pt}%
    {\techfont\tiny\color{mediumgray}\href{#1}{#2}\par}
}

% Report final page count so build.sh can enforce a single page
\AtEndDocument{\clearpage\typeout{RESUME-PAGES: \the\numexpr\value{page}-1\relax}}
