#!/bin/bash

# Build script for resume PDF
# Usage: ./build.sh

echo "Building resume PDF..."

# Compile LaTeX to PDF with XeLaTeX for modern fonts
xelatex -interaction=nonstopmode resume.tex > /dev/null 2>&1

# Clean up auxiliary files
rm -f resume.aux resume.log resume.out

if [ -f resume.pdf ]; then
    echo "✓ Resume built successfully: resume.pdf"
else
    echo "✗ Build failed. Running with verbose output:"
    xelatex -interaction=nonstopmode resume.tex
    exit 1
fi
