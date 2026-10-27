# Resume Project - Claude Code Context

## Project Overview

This is a personal resume project that maintains both a web portfolio (`index.html`) and a LaTeX resume (`resume.tex`) from a single source of truth: `data.json`.

## Architecture

### Single Source of Truth: `data.json`

All content is stored in `data.json` with the following structure:
- **personal**: Name, title, contact information (phone, email, LinkedIn, GitHub, location, websiteUrl)
- **about**: Professional summary paragraph
- **intro**: One line under the hero greeting
- **agentNote**: The "hello, agent" note in llms.txt and resume.json
- **tagline**: Extended tagline for the website hero section
- **skills**:
  - `technical`: Array of technical skills
  - `leadership`: Array of leadership skills
- **experience**: Array of companies, each with:
  - `company`: Company name
  - `tagline`: Optional one-line company descriptor (shown next to the name in the PDF)
  - `color`: Color class (company1–company4)
  - `positions`: Array of positions at that company, each with:
    - `title`: Job title
    - `dateRange`: Employment dates
    - `achievements`: Array of bullet points
- **education**: School, degree, minor, graduation date

### File Structure

```
.
├── data.json              # Single source of truth for all content
├── index.html             # Website; <!-- gen:name --> regions are filled at build
├── generate_site.py       # data.json → index.html regions, llms.txt, resume.md/.txt/.json, robots.txt, sitemap.xml
├── generate_resume.py     # data.json → resume.tex (content only, stdlib)
├── resume.cls             # PDF layout, typography, colors
├── build.sh               # Generate + compile + one-page check (--watch supported)
├── resume.tex             # Generated, gitignored
├── build/                 # Tectonic output + logs, gitignored
├── resume.pdf             # Compiled PDF resume
├── .github/workflows/build-resume.yml  # CI rebuilds resume.pdf on push
└── .claude/
    ├── claude.md          # This file
    └── settings.local.json # Claude Code permissions
```

## How to Update Content

### 1. Edit Content
Edit `data.json` to update any content (contact info, experience, skills, etc.)

### 2. Build
```bash
./build.sh
```
This validates `data.json`, fills the generated regions of `index.html`, writes `llms.txt`, the
resume formats, `robots.txt` and `sitemap.xml`, generates `resume.tex`, compiles with Tectonic,
copies the PDF to `resume.pdf`, and fails if the resume runs past one page. Logs land in `build/resume.log`.

## Development Workflow

### Preview Website Locally
```bash
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Build PDF Resume
```bash
./build.sh           # one-shot build
./build.sh --watch   # rebuild on changes (needs fswatch)
```
Requires `brew install tectonic`. Falls back to `latexmk -xelatex` if Tectonic is missing.
CI (`.github/workflows/build-resume.yml`) runs `./build.sh` and commits any changed outputs on pushes to main.

## Key Implementation Details

### Website (`index.html`)
- Content (head meta + JSON-LD, bio, links, jobs, skills, footer) is written into `index.html` by
  `generate_site.py` between `<!-- gen:name -->` markers, so crawlers and AI agents can read it without JavaScript
- Never hand-edit inside the markers; edit `data.json` or the generator and rebuild
- JavaScript only handles animation and interaction (cranes, quotes, nav, email copy, folding guide)

### LaTeX Generator (`generate_resume.py`) and class (`resume.cls`)
- The generator only emits content using macros from `resume.cls`
  (`\name`, `\contact`, `\sidebarsection`, `\skill`, `\company`, `\position`, `\achievement`, `\websiteqr`)
- All styling (fonts, colors, spacing, layout) lives in `resume.cls`; change look there, not in Python
- Escapes special LaTeX characters (\, &, %, $, #, _, {, }, ~, ^) in a single pass
- QR code (`qrcode`), sidebar dot grid and experience timeline (`tikz`) render inside LaTeX; no Python deps
- Two-column layout: sidebar (personal info, skills, education, QR) + main column (experience)
- Size macros put `\par` inside their font-size group so line spacing matches the font size

## Important Notes for Claude Code

### When Updating Content:
1. **ALWAYS** edit `data.json` first
2. Run `./build.sh` (the website won't change until you do)
3. Check the website in a browser and the PDF

### When Making Structural Changes:
- If adding new fields to `data.json`, update both:
  - `generate_site.py` (website regions and agent files)
  - The `generate_latex_resume()` function in `generate_resume.py` (and a macro in `resume.cls` if it needs new styling)
- Adding a company color: define `companyN` in `resume.cls`, add `--companyN` + a class in `index.html`
- Keep the JSON structure flat and simple for easy maintenance

### LaTeX Considerations:
- Type: Didot (name, company names), Avenir Next (body, About), Menlo (labels, dates). All macOS system fonts; build on macOS
- Special characters in `data.json` will be automatically escaped by `generate_resume.py`
- The resume must stay one page; `build.sh` enforces this

### Writing Style:
- Keep Christian's own voice: direct, plain verbs ("Built", "Developed", "Architected"), concrete specifics
- Avoid polished marketing phrasing; when trimming for space, cut clauses rather than rewording

### Design Philosophy:
- **DRY Principle**: Don't Repeat Yourself - maintain content in one place
- **Separation of Concerns**: Data (JSON) → Presentation (HTML/LaTeX)
- **Automation**: Use scripts to transform data into multiple formats

## Color Scheme

```
PDF (resume.cls)          Website (index.html)
Ink:       #1C1B1A        #000000
Accent:    #A8673A        #CC9364
Paper:     #F7F5F1  (sidebar)
Grid dots: #DDD7CE
Rule:      #D8D2C9
Dark Gray: #2E2C2A
Mid Gray:  #77716A
The PDF uses only the accent; company colors below are for the website.
company1:  #4682B4 (Slalom)
company2:  #6495ED (Triblio)
company3:  #CD5C5C (Accenture)
company4:  #3D9A8B (Parloa)
```

## Testing Checklist

Before considering changes complete:
- [ ] `data.json` is valid JSON (no syntax errors)
- [ ] Website loads and displays all content correctly
- [ ] `./build.sh` succeeds and reports 1 page
- [ ] PDF resume matches expected formatting and content
- [ ] All contact links work (phone, email, GitHub)
- [ ] No LaTeX special characters appear unescaped in PDF

## Common Tasks

### Add a New Job Position
1. Edit `data.json` → find the appropriate company in `experience` array
2. Add new position object to that company's `positions` array
3. Refresh website to verify
4. Run `./build.sh` to rebuild the PDF

### Update Skills
1. Edit `data.json` → modify `skills.technical` or `skills.leadership` arrays
2. Changes automatically appear on website refresh
3. Run `./build.sh` to rebuild the PDF

### Change Contact Information
1. Edit `data.json` → modify `personal` object
2. Refresh website to verify
3. Run `./build.sh` to rebuild the PDF

## Dependencies

### Website
- Modern web browser with JavaScript enabled
- HTTP server for local testing (Python's `http.server` is sufficient)

### Resume Generator
- Python 3.x, standard library only

### PDF Compilation
- Tectonic (`brew install tectonic`), or a TeX distribution with latexmk + XeLaTeX
- Didot, Avenir Next and Menlo (bundled with macOS)
- Packages (fetched automatically by Tectonic): fontspec, xcolor, geometry, tikz, eso-pic, enumitem, qrcode, microtype, hyperref
