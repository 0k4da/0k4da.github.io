# Christian Okada - Resume & Portfolio

This repository contains my professional resume and portfolio, available in multiple formats:

## 🌐 View Online
**Website:** [https://0k4da.github.io](https://0k4da.github.io)

Visit the live portfolio website for an interactive experience with animations and full content.

## 📄 Download PDF
**Resume PDF:** [resume.pdf](resume.pdf)

Download the PDF version for traditional applications and printing.

## 📱 Quick Access
Scan the QR code on the PDF resume to instantly access the online portfolio!

---

## About

**Christian Okada** - Software Architect
📍 San Diego, CA
📧 christian.okada@gmail.com
🐙 [@OkadaChristian](https://github.com/OkadaChristian)

Seven years architecting AI-driven solutions where simplicity meets innovation. Currently leading Slalom's AI Value Platform—transforming how organizations measure, prioritize, and deploy generative AI.

---

## Architecture

This project uses a **single source of truth** approach:
- All content is stored in `data.json`
- The website (`index.html`) dynamically loads from JSON
- The PDF resume is generated from JSON using `generate_resume.py`
- Updates to `data.json` automatically reflect across both formats

### File Structure
```
├── data.json              # Single source of truth
├── index.html             # Portfolio website
├── resume.tex             # LaTeX source
├── resume.pdf             # PDF resume
├── generate_resume.py     # Generator script
├── qr_code.png           # QR code to portfolio
└── .claude/
    └── claude.md         # Developer documentation
```

## Making Updates

1. **Edit content**: Update `data.json`
2. **Regenerate resume**: Run `python3 generate_resume.py`
3. **Compile PDF**: Run `pdflatex resume.tex`
4. **Test locally**: Run `python3 -m http.server 8000`
5. **Deploy**: Commit and push to GitHub

---

*Built with Claude Code*
