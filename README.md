# Christian Okada - Resume As Code

> Maintaining a professional resume and portfolio using infrastructure-as-code principles: one source of truth, version controlled, and programmatically generated.

## 🌐 View My Work

**Portfolio Website:** [https://0k4da.github.io](https://0k4da.github.io)
**Resume PDF:** [resume.pdf](resume.pdf)

---

## 👋 About Me

**Christian Okada** - Software Architect
📍 San Diego, CA
📧 christian.okada@gmail.com
💼 [LinkedIn: OkadaChristian](https://linkedin.com/in/OkadaChristian)

Seven years architecting AI-driven solutions where simplicity meets innovation. Currently leading Slalom's AI Value Platform—transforming how organizations measure, prioritize, and deploy generative AI.

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
data.json  ─┬─→ index.html (live website)
            └─→ generate_resume.py → resume.tex → resume.pdf
```

All content lives in [`data.json`](data.json):
- Personal information and contact details
- Professional summary and tagline
- Technical and leadership skills
- Work experience with achievements
- Education

The website dynamically loads from JSON. The PDF resume is generated via Python script and compiled with LaTeX.

### Project Structure

```
├── data.json              # Single source of truth for all content
├── index.html             # Interactive portfolio website
├── generate_resume.py     # LaTeX generator script
├── resume.pdf             # Generated PDF resume
├── qr_code.png           # QR code linking to portfolio
├── build.sh              # Build automation script
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

**Update Content:**
```bash
# 1. Edit the data
vim data.json

# 2. Generate LaTeX source
python3 generate_resume.py

# 3. Compile to PDF
pdflatex resume.tex

# 4. Test website locally
python3 -m http.server 8000
```

**Deploy:**
```bash
git add data.json resume.pdf
git commit -m "Update resume"
git push
```

The website auto-updates via GitHub Pages. No build step needed—it loads `data.json` directly.

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
- Vanilla JavaScript with async/await
- Dynamically populates from `data.json`
- Responsive design with smooth animations
- No build tools or frameworks required

**PDF Generator:**
- Python script with LaTeX templating
- Automatic escaping of special characters
- Two-column layout with color-coded sections
- Professional typography using Helvetica Neue

**Stack:**
- Python 3.x (generator script)
- LaTeX (XeLaTeX/LuaLaTeX for PDF compilation)
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
