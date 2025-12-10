#!/usr/bin/env bash
# Build script for Render deployment

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p instance
mkdir -p static/chords
mkdir -p static/slides
mkdir -p static/profiles/pictures
mkdir -p static/profiles/banners
mkdir -p static/profiles/backgrounds
mkdir -p static/profiles/posts
mkdir -p static/announcements
mkdir -p static/journals
mkdir -p static/tools

echo "Build completed successfully!"

