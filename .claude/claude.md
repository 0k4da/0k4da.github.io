# Resume Project - Claude Code Context

## Project Overview

This is a personal resume project that maintains both a web portfolio (`index.html`) and a LaTeX resume (`resume.tex`) from a single source of truth: `data.json`.

## Architecture

### Single Source of Truth: `data.json`

All content is stored in `data.json` with the following structure:
- **personal**: Name, title, contact information (phone, email, GitHub, location)
- **about**: Professional summary paragraph
- **tagline**: Extended tagline for the website hero section
- **skills**:
  - `technical`: Array of technical skills
  - `leadership`: Array of leadership skills
- **experience**: Array of companies, each with:
  - `company`: Company name
  - `color`: CSS color class (company1, company2, company3)
  - `positions`: Array of positions at that company, each with:
    - `title`: Job title
    - `dateRange`: Employment dates
    - `achievements`: Array of bullet points
- **education**: School, degree, minor, graduation date

### File Structure

```
.
├── data.json              # Single source of truth for all content
├── index.html             # Website portfolio (loads from data.json)
├── resume.tex             # LaTeX resume (generated from data.json)
├── resume.pdf             # Compiled PDF resume
├── generate_resume.py     # Python script to generate resume.tex from data.json
└── .claude/
    ├── claude.md          # This file
    └── settings.local.json # Claude Code permissions
```

## How to Update Content

### 1. Edit Content
Edit `data.json` to update any content (contact info, experience, skills, etc.)

### 2. Update Website
The website automatically loads from `data.json` - no additional steps needed. Just refresh the page.

### 3. Update Resume
Run the generator script to rebuild `resume.tex`:
```bash
python3 generate_resume.py
```

Then compile the LaTeX to PDF (if needed):
```bash
pdflatex resume.tex
```

## Development Workflow

### Preview Website Locally
```bash
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Build PDF Resume
```bash
python3 generate_resume.py  # Generate .tex from data.json
pdflatex resume.tex         # Compile to PDF
```

### Build Script
There's a `build.sh` script that handles the full build process (approved in Claude Code permissions).

## Key Implementation Details

### Website (`index.html`)
- Uses vanilla JavaScript with async/await to fetch `data.json`
- Dynamically populates all content on page load via `loadData()` function
- Maintains all existing animations, styling, and interactivity
- All dynamic content elements have IDs for DOM manipulation

### LaTeX Generator (`generate_resume.py`)
- Reads `data.json` and generates formatted LaTeX
- Properly escapes special LaTeX characters (&, %, $, #, _, {, }, ~, ^)
- Maintains consistent styling with color scheme:
  - Primary: Black (#000000)
  - Accent: Gold (#CC9364)
  - Company colors: Blue shades for Slalom/Triblio, Red for Accenture
- Two-column layout: sidebar (personal info, skills, education) + main content (experience)

## Important Notes for Claude Code

### When Updating Content:
1. **ALWAYS** edit `data.json` first
2. Test the website by loading it in a browser
3. Run `generate_resume.py` to update the LaTeX
4. Verify the generated `resume.tex` compiles correctly

### When Making Structural Changes:
- If adding new fields to `data.json`, update both:
  - The `loadData()` function in `index.html`
  - The `generate_latex_resume()` function in `generate_resume.py`
- Keep the JSON structure flat and simple for easy maintenance

### LaTeX Considerations:
- The resume uses `fontspec` and requires XeLaTeX or LuaLaTeX (uses Helvetica Neue font)
- Special characters in `data.json` will be automatically escaped by `generate_resume.py`
- Color classes (company1, company2, company3) map to specific companies

### Design Philosophy:
- **DRY Principle**: Don't Repeat Yourself - maintain content in one place
- **Separation of Concerns**: Data (JSON) → Presentation (HTML/LaTeX)
- **Automation**: Use scripts to transform data into multiple formats

## Color Scheme

```
Primary Black:    #000000
Accent Gold:      #CC9364
Sidebar BG:       #F5FAFA
Dark Gray:        #282828
Medium Gray:      #646464
Light Gray:       #F0F0F0
Company Blue 1:   #4682B4 (Slalom)
Company Blue 2:   #6495ED (Triblio)
Company Red:      #CD5C5C (Accenture)
```

## Testing Checklist

Before considering changes complete:
- [ ] `data.json` is valid JSON (no syntax errors)
- [ ] Website loads and displays all content correctly
- [ ] `generate_resume.py` runs without errors
- [ ] Generated `resume.tex` compiles to PDF successfully
- [ ] PDF resume matches expected formatting and content
- [ ] All contact links work (phone, email, GitHub)
- [ ] No LaTeX special characters appear unescaped in PDF

## Common Tasks

### Add a New Job Position
1. Edit `data.json` → find the appropriate company in `experience` array
2. Add new position object to that company's `positions` array
3. Refresh website to verify
4. Run `python3 generate_resume.py` to update LaTeX

### Update Skills
1. Edit `data.json` → modify `skills.technical` or `skills.leadership` arrays
2. Changes automatically appear on website refresh
3. Run `python3 generate_resume.py` to update LaTeX

### Change Contact Information
1. Edit `data.json` → modify `personal` object
2. Refresh website to verify
3. Run `python3 generate_resume.py` to update LaTeX

## Dependencies

### Website
- Modern web browser with JavaScript enabled
- HTTP server for local testing (Python's `http.server` is sufficient)

### Resume Generator
- Python 3.x
- Standard library only (no external dependencies)

### PDF Compilation
- LaTeX distribution with XeLaTeX or LuaLaTeX
- Helvetica Neue font installed on system
- Required LaTeX packages: fontspec, xcolor, geometry, inputenc
