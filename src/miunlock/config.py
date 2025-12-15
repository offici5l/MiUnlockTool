import os
import platform
import shutil
import stat
from pathlib import Path
import urllib.request
import zipfile
import subprocess
import requests

SYSTEM = platform.system()

def make_executable(path):
    if SYSTEM in ["Linux", "Darwin"]:
        try:
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)
        except Exception as e:
            print(f"\nWarning: Could not make {path} executable: {e}\n")

def install_termux_fastboot():
    print('\nfastboot is not installed! It will now be installed from repo: https://github.com/nohajc/termux-adb ...\n')
    
    try:
        print("\nUpdating System & Fixing Broken Packages...\n")
        result = subprocess.run(
            "yes | apt --fix-broken install && yes | apt update && yes | apt upgrade",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {'error': f'System update failed: {result.stderr or result.stdout}'}
        
        print("\nInstalling fastboot...\n")
        response = requests.get("https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh")
        
        if response.status_code != 200:
            return {'error': f'Failed to download install script: HTTP {response.status_code}'}
        
        result = subprocess.run(
            response.text,
            shell=True,
            capture_output=True,
            text=True,
            executable='/data/data/com.termux/files/usr/bin/bash'
        )
        
        if result.returncode != 0:
            return {'error': f'Installation failed: {result.stderr or result.stdout}'}
        
        return {'success': True}
        
    except requests.RequestException as e:
        return {'error': f'Network error: {str(e)}'}
    except Exception as e:
        return {'error': f'Installation error: {str(e)}'}


def config_termux():
    try:
        config_file = Path.home() / '.termux' / 'termux.properties'
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        existing_content = ""
        if config_file.exists():
            existing_content = config_file.read_text(encoding='utf-8')
        
        if "allow-external-apps = true" not in existing_content:
            with open(config_file, 'a', encoding='utf-8') as f:
                f.write("\nallow-external-apps = true\n")
            subprocess.run(['termux-reload-settings'], check=False)
        
        result = subprocess.run(
            ["cmd", "package", "list", "packages", "com.termux.api"],
            capture_output=True,
            text=True
        )
        
        if "package:com.termux.api" not in result.stdout:
            return {"error": "com.termux.api app is not installed! Download it from https://github.com/termux/termux-api/releases/latest first and run miunlock again after installation"}
        
        PREFIX = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')
        fastboot_path = f"{PREFIX}/bin/termux-fastboot"
        
        if not os.path.isfile(fastboot_path):
            install_result = install_termux_fastboot()
            
            if isinstance(install_result, dict) and "error" in install_result:
                return install_result
            
            if not os.path.isfile(fastboot_path):
                return {"error": "Failed to install termux-fastboot"}
        
        make_executable(fastboot_path)
        return {"path": fastboot_path}
        
    except Exception as e:
        return {"error": f"Termux configuration error: {str(e)}"}


def download_platform_tools():
    system_map = {
        "Linux": "linux",
        "Darwin": "darwin",
        "Windows": "windows"
    }
    
    os_name = system_map.get(SYSTEM)
    if not os_name:
        return {"error": f"Unsupported operating system: {SYSTEM}"}
    
    url = f"https://dl.google.com/android/repository/platform-tools-latest-{os_name}.zip"
    tools_dir = Path.home() / "platform-tools"
    zip_path = tools_dir.parent / "platform-tools.zip"
    
    print(f"\nDownloading platform-tools for {os_name} from {url} ...\n")
    
    try:
        tools_dir.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, str(zip_path))
        
        print("\nExtracting platform-tools...\n")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(str(tools_dir.parent))
        
        zip_path.unlink()
        
        fastboot_path = tools_dir / "fastboot"
        if SYSTEM == "Windows":
            fastboot_path = tools_dir / "fastboot.exe"
        
        if not fastboot_path.exists():
            return {"error": "Fastboot binary not found after extraction"}
        
        make_executable(str(fastboot_path))
        return {"path": str(fastboot_path)}
        
    except urllib.error.URLError as e:
        return {"error": f"Download failed: {str(e)}"}
    except zipfile.BadZipFile:
        return {"error": "Downloaded file is corrupted"}
    except Exception as e:
        return {"error": f"Failed to download platform-tools: {str(e)}"}


def config_s():
    try:
        if SYSTEM == "Linux" and os.path.exists("/data/data/com.termux"):
            return config_termux()
        
        cmd = shutil.which("fastboot")
        if cmd is not None:
            make_executable(cmd)
            return {"path": cmd}
        
        tools_dir = Path.home() / "platform-tools"
        fastboot_path = tools_dir / "fastboot"
        
        if SYSTEM == "Windows":
            fastboot_path = tools_dir / "fastboot.exe"
        
        if fastboot_path.exists():
            make_executable(str(fastboot_path))
            return {"path": str(fastboot_path)}
        
        print('\nfastboot is not installed!\n')
        return download_platform_tools()
        
    except Exception as e:
        return {"error": f"Error checking fastboot: {str(e)}"}