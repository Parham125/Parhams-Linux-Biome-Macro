import os
import sys
import subprocess
import shutil
import tempfile
import requests
import zipfile
from pathlib import Path
from tkinter import messagebox
GITHUB_REPO="Parham125/Parhams-Linux-Biome-Macro"
GITHUB_API_URL=f"https://api.github.com/repos/{GITHUB_REPO}/commits/main"
GITHUB_ZIP_URL=f"https://github.com/{GITHUB_REPO}/archive/refs/heads/main.zip"
VERSION_FILE="VERSION"
def get_current_version():
    version_path=Path(__file__).parent/VERSION_FILE
    if version_path.exists():
        return version_path.read_text().strip()
    return None
def get_latest_version():
    try:
        response=requests.get(GITHUB_API_URL,timeout=10)
        response.raise_for_status()
        return response.json()["sha"]
    except Exception as e:
        raise Exception(f"Failed to check for updates: {str(e)}")
def is_git_repo():
    git_dir=Path(__file__).parent/".git"
    return git_dir.exists()
def update_via_git():
    try:
        result=subprocess.run(["git","pull","origin","main"],capture_output=True,text=True,cwd=Path(__file__).parent)
        if result.returncode!=0:
            raise Exception(f"Git pull failed: {result.stderr}")
        result=subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True,cwd=Path(__file__).parent)
        if result.returncode==0:
            new_version=result.stdout.strip()
            (Path(__file__).parent/VERSION_FILE).write_text(new_version)
        return True
    except Exception as e:
        raise Exception(f"Git update failed: {str(e)}")
def update_via_zip():
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path=Path(temp_dir)/"repo.zip"
            response=requests.get(GITHUB_ZIP_URL,timeout=30)
            response.raise_for_status()
            zip_path.write_bytes(response.content)
            with zipfile.ZipFile(zip_path,"r") as zip_ref:
                zip_ref.extractall(temp_dir)
            extracted_dir=Path(temp_dir)/"Parhams-Linux-Biome-Macro-main"
            if not extracted_dir.exists():
                raise Exception("Extracted directory not found")
            current_dir=Path(__file__).parent
            for item in extracted_dir.iterdir():
                if item.name in [".git",".gitignore","config.json","VERSION"]:
                    continue
                dest=current_dir/item.name
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                if item.is_dir():
                    shutil.copytree(item,dest)
                else:
                    shutil.copy2(item,dest)
            latest_version=get_latest_version()
            (current_dir/VERSION_FILE).write_text(latest_version)
        return True
    except Exception as e:
        raise Exception(f"ZIP update failed: {str(e)}")
def restart_app():
    python=sys.executable
    os.execl(python,python,*sys.argv)
def check_and_update():
    try:
        current_version=get_current_version()
        latest_version=get_latest_version()
        if current_version and not current_version[0].isdigit():
            if current_version==latest_version:
                return False
        else:
            (Path(__file__).parent/VERSION_FILE).write_text(latest_version)
            return False
        if is_git_repo():
            update_via_git()
        else:
            update_via_zip()
        return True
    except Exception as e:
        messagebox.showerror("Update Failed",f"Failed to update the application:\n\n{str(e)}\n\nThe application will now close.")
        sys.exit(1)
def auto_update():
    try:
        updated=check_and_update()
        if updated:
            messagebox.showinfo("Update Complete","The application has been updated. It will now restart.")
            restart_app()
    except Exception as e:
        messagebox.showerror("Update Failed",f"Failed to update the application:\n\n{str(e)}\n\nThe application will now close.")
        sys.exit(1)
