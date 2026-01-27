#!/usr/bin/env python3
import os
import zipfile
from pathlib import Path

PROJECT = "geopunt4Qgis"
INCLUDE_EXTENSIONS = {".py", 'LICENSE', ".txt", ".qrc", ".md", ".gif", ".jpg", ".png", ".html", ".qm", ".json", ".xml"}
INCLUDE_DIRS = {"images", "i18n", "data", "tools", "geopunt", "mapTools"}

def get_file_list(src_path):
    """Generates the list of files based on directory and extension filters."""
    file_list = []
    
    # Recursive search in specific directories
    for folder in INCLUDE_DIRS:
        folder_path = src_path / folder
        if folder_path.exists():
            file_list.extend([f for f in folder_path.rglob('*') if f.is_file()])
        
    # Search for specific file types in the root
    for ext in INCLUDE_EXTENSIONS:
        file_list.extend([f for f in src_path.glob(f"*{ext}") if f.is_file()])
        
    return file_list

def main():
    # SOURCE is the folder containing the plugin code
    source_dir = Path(__file__).resolve().parent.parent
    target_dir = source_dir / "build"
    target_zip = target_dir / f"{PROJECT}.zip"

    target_dir.mkdir(parents=True, exist_ok=True)
    
    if target_zip.exists():
        target_zip.unlink()

    print(f"Creating archive: {target_zip}")

    with zipfile.ZipFile(target_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for file_path in get_file_list(source_dir):
            relative_path = file_path.relative_to(source_dir)
            arc_name = Path(PROJECT) / relative_path
            zipf.write(file_path, arcname=arc_name)

if __name__ == '__main__':
    main()