#!/bin/bash
echo "Building Parham's Linux Biome Macro..."
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi
pyinstaller --name="BiomeMacro" \
    --onefile \
    --windowed \
    --add-data "assets:assets" \
    --add-data "biome_data.py:." \
    --hidden-import="PIL._tkinter_finder" \
    --collect-all customtkinter \
    main.py
echo "Build complete! Executable is in dist/BiomeMacro"
