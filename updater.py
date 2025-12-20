import os
import sys
import subprocess
import tempfile
import requests
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from utils import get_resource_path
GITHUB_REPO="Parham125/Parhams-Linux-Biome-Macro"
GITHUB_RELEASES_URL=f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
VERSION_FILE="VERSION"
def get_current_version():
    version_path=Path(get_resource_path(VERSION_FILE))
    if version_path.exists():
        return version_path.read_text().strip()
    return None
def get_latest_release():
    try:
        response=requests.get(GITHUB_RELEASES_URL,timeout=10)
        response.raise_for_status()
        data=response.json()
        return {"tag": data["tag_name"].lstrip("v"),"download_url": None}
    except Exception as e:
        raise Exception(f"Failed to check for updates: {str(e)}")
def get_binary_download_url():
    try:
        response=requests.get(GITHUB_RELEASES_URL,timeout=10)
        response.raise_for_status()
        data=response.json()
        for asset in data.get("assets",[]):
            if asset["name"]=="BiomeMacro":
                return asset["browser_download_url"]
        raise Exception("Binary not found in latest release")
    except Exception as e:
        raise Exception(f"Failed to get download URL: {str(e)}")
def compare_versions(current,latest):
    try:
        current_parts=[int(x) for x in current.split(".")]
        latest_parts=[int(x) for x in latest.split(".")]
        return latest_parts>current_parts
    except:
        return current!=latest
def download_and_replace_binary(download_url):
    try:
        current_exe=Path(sys.executable).resolve()
        with tempfile.NamedTemporaryFile(delete=False,suffix=".tmp") as temp_file:
            temp_path=Path(temp_file.name)
        response=requests.get(download_url,timeout=60,stream=True)
        response.raise_for_status()
        temp_path.write_bytes(response.content)
        temp_path.chmod(0o755)
        update_script=current_exe.parent/"update.sh"
        script_content=f"""#!/bin/bash
sleep 2
mv "{temp_path}" "{current_exe}"
chmod +x "{current_exe}"
"{current_exe}" &
rm "$0"
"""
        update_script.write_text(script_content)
        update_script.chmod(0o755)
        subprocess.Popen([str(update_script)],start_new_session=True)
        return True
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise Exception(f"Failed to download and replace binary: {str(e)}")
def show_message(title,message,message_type="info"):
    root=tk.Tk()
    root.withdraw()
    if message_type=="info":
        messagebox.showinfo(title,message)
    elif message_type=="error":
        messagebox.showerror(title,message)
    root.destroy()
def check_and_update():
    try:
        if not getattr(sys,"frozen",False):
            return False
        current_version=get_current_version()
        if not current_version:
            return False
        latest_release=get_latest_release()
        latest_version=latest_release["tag"]
        if not compare_versions(current_version,latest_version):
            return False
        download_url=get_binary_download_url()
        download_and_replace_binary(download_url)
        return True
    except Exception as e:
        show_message("Update Failed",f"Failed to update the application:\n\n{str(e)}\n\nThe application will now close.","error")
        sys.exit(1)
def auto_update():
    try:
        updated=check_and_update()
        if updated:
            show_message("Update Complete","The application has been updated. It will now restart.","info")
            sys.exit(0)
    except Exception as e:
        show_message("Update Failed",f"Failed to update the application:\n\n{str(e)}\n\nThe application will now close.","error")
        sys.exit(1)
