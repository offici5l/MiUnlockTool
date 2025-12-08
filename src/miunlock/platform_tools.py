import os
import platform
import shutil
import stat
from pathlib import Path
import urllib.request
import zipfile
import subprocess

s = platform.system()

def check_fastboot():
    if s == "Linux" and os.path.exists("/data/data/com.termux"):

        config_file = Path.home() / '.termux' / 'termux.properties'
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'a', encoding='utf-8') as f:
            f.write("\nallow-external-apps = true\n")
        os.system('termux-reload-settings')

        if subprocess.run(["cmd", "package", "list", "packages", "com.termux.api"], capture_output=True, text=True).stdout.strip() != "package:com.termux.api":
            return {"error": "com.termux.api app is not installed\nPlease install it first"}

        PREFIX = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')
        fastboot_path = f"{PREFIX}/bin/termux-fastboot"

        if not os.path.isfile(fastboot_path):
            return {
                "error": "termux-fastboot is not installed\n\n"
                "Please install it manually from:\n"
                "https://github.com/nohajc/termux-adb\n\n"
                "Then run miunlock again"
            }

        return fastboot_path

    cmd = shutil.which("fastboot")        
    if cmd is not None:
        return cmd

    tools_dir = Path.home() / "platform-tools"
    
    fastboot_path = tools_dir / "fastboot"
    if s == "Windows":
        fastboot_path = tools_dir / "fastboot.exe"

    if fastboot_path.exists():
        if s in ["Linux", "Darwin"]:
            st = os.stat(fastboot_path)
            os.chmod(fastboot_path, st.st_mode | stat.S_IEXEC)
        
        return str(fastboot_path)

    print("\nDownloading platform-tools...")
    
    system_map = {
        "Linux": "linux",
        "Darwin": "darwin",
        "Windows": "windows"
    }
    
    os_name = system_map.get(s, s.lower())
    url = f"https://dl.google.com/android/repository/platform-tools-latest-{os_name}.zip"

    tools_dir.parent.mkdir(parents=True, exist_ok=True)
    zip_path = tools_dir.parent / "platform-tools.zip"

    try:
        urllib.request.urlretrieve(url, str(zip_path))

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(str(tools_dir.parent))

        zip_path.unlink()

        if s in ["Linux", "Darwin"]:
            st = os.stat(fastboot_path)
            os.chmod(fastboot_path, st.st_mode | stat.S_IEXEC)

        return str(fastboot_path)

    except Exception as e:
        return {"error": f"Failed to download platform-tools: {str(e)}"}