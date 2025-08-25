#!/bin/bash

echo "Creating data directory structure..."

mkdir -p data

mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/interim
mkdir -p data/external

touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/interim/.gitkeep
touch data/external/.gitkeep

echo "Data directory structure created successfully!"
echo "Directory structure:"
tree data/ 2>/dev/null || find data -type d | sed 's|[^/]*/|  |g'