#!/usr/bin/env bash
# Render build script for FastAPI service

set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating ChromaDB directory..."
mkdir -p /app/chroma_db

echo "Build completed successfully!"
