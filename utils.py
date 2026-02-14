import sys
import os
from pathlib import Path
def get_resource_path(relative_path):
    if hasattr(sys,"_MEIPASS"):
        return os.path.join(sys._MEIPASS,relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),relative_path)
def get_version():
    version_path=Path(get_resource_path("VERSION"))
    if version_path.exists():
        return version_path.read_text().strip()
    return "Unknown"
