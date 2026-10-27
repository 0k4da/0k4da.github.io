#!/usr/bin/env bash
# Build resume.pdf from data.json.
#
# Usage:
#   ./build.sh          generate resume.tex and compile resume.pdf
#   ./build.sh --watch  rebuild whenever data.json, resume.cls or the generator changes
#
# Requires Python 3 and Tectonic (brew install tectonic). Falls back to
# latexmk/xelatex if Tectonic isn't installed.
set -euo pipefail
cd "$(dirname "$0")"

BUILD_DIR=build
WATCHED=(data.json resume.cls generate_resume.py)

build() {
    python3 -c 'import json; json.load(open("data.json"))' \
        || { echo "✗ data.json is not valid JSON"; return 1; }
    python3 generate_resume.py
    mkdir -p "$BUILD_DIR"

    echo "Compiling PDF..."
    if command -v tectonic >/dev/null; then
        tectonic --chatter minimal --keep-logs --outdir "$BUILD_DIR" resume.tex \
            || { echo "✗ Build failed (full log: $BUILD_DIR/resume.log)"; return 1; }
    elif command -v latexmk >/dev/null; then
        latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$BUILD_DIR" resume.tex >/dev/null \
            || { tail -n 30 "$BUILD_DIR/resume.log"; echo "✗ Build failed"; return 1; }
    else
        echo "✗ No LaTeX engine found. Install one with: brew install tectonic"
        return 1
    fi

    cp "$BUILD_DIR/resume.pdf" resume.pdf

    pages=$(sed -n 's/^RESUME-PAGES: \([0-9]*\)$/\1/p' "$BUILD_DIR/resume.log" | tail -n 1)
    if [[ "${pages:-1}" -gt 1 ]]; then
        echo "✗ Resume spilled onto $pages pages; trim content in data.json"
        return 1
    fi
    echo "✓ Built resume.pdf (${pages:-1} page)"
}

if [[ "${1:-}" == "--watch" ]]; then
    command -v fswatch >/dev/null || { echo "Install fswatch for watch mode: brew install fswatch"; exit 1; }
    build || true
    echo "Watching ${WATCHED[*]} for changes (Ctrl-C to stop)..."
    fswatch -o "${WATCHED[@]}" | while read -r _; do build || true; done
else
    build
fi
