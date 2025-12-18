#!/bin/bash
echo "Building Parham's Linux Biome Macro with Docker..."
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    echo "Docker installed. You may need to log out and back in for group changes to take effect."
    echo "Please run this script again after logging back in."
    exit 1
fi
echo "Building Docker image..."
docker build -t biome-macro-builder .
echo "Building executable in Docker container..."
docker run --rm -v "$(pwd)/dist:/app/dist" biome-macro-builder
echo "Build complete! Executable is in dist/BiomeMacro"
