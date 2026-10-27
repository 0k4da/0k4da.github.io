# Christian Okada - Resume As Code

> Maintaining a professional resume and portfolio using infrastructure-as-code principles: one source of truth, version controlled, and programmatically generated.

## 🌐 View My Work

**Portfolio Website:** [https://0k4da.github.io](https://0k4da.github.io)
**Resume PDF:** [resume.pdf](resume.pdf)

---

## 👋 About Me

**Christian Okada** - Lead Go-to-Market Engineer @ Parloa
📍 Washington, DC
📧 christian.okada@gmail.com
💼 [LinkedIn: OkadaChristian](https://linkedin.com/in/OkadaChristian)

Eight years building software: DevOps for a large federal client, cloud architecture, then leading Slalom's AI Value Platform. Now I lead go-to-market engineering at Parloa, where I built and run the go-to-market engine and the context engine, along with the pricing framework and ROI business cases behind every deal.

---

## 💡 The "Resume As Code" Concept

This repository treats my resume like infrastructure—maintaining a **single source of truth** and generating multiple output formats programmatically.

### Why This Approach?

- **DRY Principle**: Update content once in `data.json`, deploy everywhere
- **Version Control**: Full Git history of my professional experience
- **Automation**: Scripts transform data into beautiful HTML and PDF formats
- **Consistency**: Website and PDF resume always stay in sync
- **Transparency**: Public codebase demonstrates engineering practices

### Architecture

```
data.json  ─┬─→ generate_site.py → index.html content, llms.txt, resume.md/.txt/.json, robots.txt, sitemap.xml
            └─→ generate_resume.py → resume.tex ─(resume.cls + Tectonic)→ resume.pdf
```

All content lives in [`data.json`](data.json):
- Personal information and contact details
- Professional summary and tagline
- Technical and leadership skills
- Work experience with achievements
- Education

The website's content is written into `index.html` at build time, so it reads fully without JavaScript (for crawlers and AI agents); JavaScript only runs the animations. The PDF resume is generated via Python script and compiled with LaTeX. All PDF styling lives in `resume.cls`; the generator only emits content.

### Project Structure

```
├── data.json              # Single source of truth for all content
├── index.html             # Interactive portfolio website (content regions filled at build)
├── generate_site.py       # data.json → index.html content + files for agents and crawlers
├── generate_resume.py     # data.json → resume.tex (content only)
├── llms.txt               # Generated: summary for AI agents, with a hello
├── resume.md / .txt / .json   # Generated: resume formats (JSON Resume schema)
├── robots.txt, sitemap.xml    # Generated: crawler access, AI crawlers welcome
├── resume.cls             # PDF layout, typography, colors
├── build.sh               # Generate + compile + one-page check
├── resume.pdf             # Generated PDF resume
├── sig/                   # Public-domain signatures for the site's rotating quotes
├── .github/workflows/     # CI: rebuilds the PDF and site files on push
└── .claude/
    └── claude.md          # Developer documentation
```

---

## 🛠 How It Works

### For Visitors

1. Visit the [live website](https://0k4da.github.io) for the full interactive experience
2. Download the [PDF resume](resume.pdf) for traditional applications
3. Scan the QR code on the PDF to jump back to the website

### For Developers

Want to build your own "Resume As Code"? Here's how mine works:

**Setup (once):**
```bash
brew install tectonic   # self-contained LaTeX engine; fetches packages on demand
brew install fswatch    # optional, for --watch
```

**Update Content:**
```bash
# 1. Edit the data
vim data.json

# 2. Build (validates JSON, fills index.html, writes llms.txt and resume formats, compiles the PDF, fails if > 1 page)
./build.sh

#    ...or rebuild automatically on every save
./build.sh --watch

# 3. Test website locally
python3 -m http.server 8000
```

**Deploy:**
```bash
git add -A
git commit -m "Update resume"
git push
```

The website auto-updates via GitHub Pages.

Pushing changes to `data.json`, `resume.cls`, `generate_resume.py`, `generate_site.py` or `build.sh` also triggers the **Build resume and site** GitHub Action, which runs `./build.sh` on a macOS runner and commits any changed outputs back. Committing them yourself is optional.

---

## 🎨 Design Principles

- **Single Source of Truth**: All content in `data.json`
- **Separation of Concerns**: Data (JSON) → Presentation (HTML/LaTeX)
- **Automation**: Scripts handle transformation and formatting
- **Accessibility**: Web-first design with PDF fallback
- **Maintainability**: Clean code, clear documentation

---

## 📝 Technical Details

**Website:**
- Content baked in from `data.json` at build time; readable without JavaScript
- `llms.txt`, schema.org JSON-LD and JSON Resume for AI agents and crawlers
- Vanilla JavaScript for the animations
- Responsive design with smooth animations
- No build tools or frameworks required

**PDF Generator:**
- Python script (standard library only) emitting content macros
- `resume.cls` class file owns layout, colors and typography
- Automatic escaping of special characters
- QR code, dot-grid sidebar, timeline and clickable links rendered natively in LaTeX
- Build fails if the resume spills past one page
- Typography: Didot for display, Avenir Next for text, Menlo for technical labels

**Stack:**
- Python 3.x (generator script)
- LaTeX via Tectonic (falls back to latexmk + XeLaTeX)
- GitHub Actions (PDF CI)
- GitHub Pages (hosting)
- Git (version control)

---

## 🤝 Get In Touch

If this "Resume As Code" approach resonates with you, or if you'd like to discuss software architecture, AI platforms, or engineering best practices:

📧 **Email:** christian.okada@gmail.com
💼 **LinkedIn:** [OkadaChristian](https://linkedin.com/in/OkadaChristian)
🌐 **Portfolio:** [0k4da.github.io](https://0k4da.github.io)

---

*Built with [Claude Code](https://claude.com/claude-code) • Open Source • [View on GitHub](https://github.com/0k4da/0k4da.github.io)*
