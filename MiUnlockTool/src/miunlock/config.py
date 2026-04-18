import os
import platform
import shutil
import stat
from pathlib import Path
import urllib.request
import urllib.error
import zipfile
import subprocess
import tempfile
from migate.config import (
    console
)


SYSTEM = platform.system()

def make_executable(path):
    if SYSTEM in ["Linux", "Darwin", "Android"]:
        try:
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)
        except Exception as e:
            console.print(f"[red]✗ Could not make {path} executable: {e}[/red]")
            raise SystemExit(1)


def download_platform_tools_termux():
    URL = "https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh"
    PREFIX = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')

    def run_script():
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(script)
                tmp_path = f.name

            yes_proc = subprocess.Popen(["yes"], stdout=subprocess.PIPE)
            proc = subprocess.run(
                ["bash", tmp_path],
                stdin=yes_proc.stdout,
                capture_output=True,
                text=True,
                env={**os.environ},
            )
            yes_proc.kill()
            return proc
        except FileNotFoundError:
            console.print("[red]✗ bash not found on this system[/red]")
            raise SystemExit(1)
        except Exception as e:
            console.print(f"[red]✗ Execution error:[/red] {e}")
            raise SystemExit(1)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    try:
        with console.status("[white]Installing termux-adb (first time only) ...[/white]"):
            gpg_url = "https://nohajc.github.io/nohajc.gpg"
            gpg_path = f"{PREFIX}/etc/apt/trusted.gpg.d/nohajc.gpg"
            os.makedirs(os.path.dirname(gpg_path), exist_ok=True)
            with urllib.request.urlopen(gpg_url, timeout=30) as resp:
                with open(gpg_path, 'wb') as f:
                    f.write(resp.read())

            with urllib.request.urlopen(URL, timeout=30) as resp:
                script = resp.read().decode("utf-8")

            proc = run_script()

            fastboot_path = f"{PREFIX}/bin/termux-fastboot"
            if not os.path.isfile(fastboot_path):
                console.print(f"\n[red]✗ Installation failed:\n{proc.stderr}\n[/red]")
                raise SystemExit(1)

    except urllib.error.HTTPError as e:
        console.print(f"[red]✗ HTTP error {e.code}:[/red] {e.reason}")
        raise SystemExit(1)
    except urllib.error.URLError as e:
        console.print(f"[red]✗ Connection failed:[/red] {e.reason}")
        raise SystemExit(1)


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
            ["cmd", "package", "list", "packages", "--user", "0", "com.termux.api"],
            capture_output=True,
            text=True
        )

        if "package:com.termux.api" not in result.stdout:
            console.print(f"\n[red]✗ com.termux.api is not installed!\nDownload it from https://github.com/termux/termux-api/releases/latest and rerun the tool.\n[/red]")
            raise SystemExit(1)

        PREFIX = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')
        fastboot_path = f"{PREFIX}/bin/termux-fastboot"

        if not os.path.isfile(fastboot_path):
            download_platform_tools_termux()

        make_executable(fastboot_path)
        return str(fastboot_path)

    except Exception as e:
        console.print(f"\n[red]✗ Termux configuration error: {str(e)}\n[/red]")
        raise SystemExit(1)



def download_platform_tools():
    system_map = {
        "Linux": "linux",
        "Darwin": "darwin",
        "Windows": "windows"
    }

    os_name = system_map.get(SYSTEM)
    if not os_name:
        console.print(f"[red]✗ platform-tools do not support this {SYSTEM}, please manually install a fastboot version compatible with your system, then restart the tool again[/red]")
        raise SystemExit(1)

    url = f"https://dl.google.com/android/repository/platform-tools-latest-{os_name}.zip"
    tools_dir = Path.home() / "platform-tools"
    zip_path = tools_dir.parent / "platform-tools.zip"

    try:
        with console.status(f"[white]Installing platform-tools for {os_name} (first time only) ...[/white]"):
            tools_dir.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(url, str(zip_path))

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(str(tools_dir.parent))

            zip_path.unlink()

            fastboot_path = tools_dir / ("fastboot.exe" if SYSTEM == "Windows" else "fastboot")
            make_executable(str(fastboot_path))
            return str(fastboot_path)

    except urllib.error.URLError as e:
        console.print(f"[red]✗ Download failed: {e}[/red]")
        raise SystemExit(1)
    except zipfile.BadZipFile:
        console.print("[red]✗ Downloaded file is corrupted[/red]")
        raise SystemExit(1)
    except Exception as e:
        console.print(f"[red]✗ Failed to download platform-tools: {e}[/red]")
        raise SystemExit(1)

def get_fastboot():
    try:
        if (SYSTEM == "Linux" or SYSTEM == "Android") and os.path.exists("/data/data/com.termux"):
            return config_termux()

        cmd = shutil.which("fastboot")
        if cmd is not None:
            make_executable(cmd)
            return str(cmd)

        tools_dir = Path.home() / "platform-tools"
        fastboot_path = tools_dir / ("fastboot.exe" if SYSTEM == "Windows" else "fastboot")

        if fastboot_path.exists():
            make_executable(str(fastboot_path))
            return str(fastboot_path)

        console.print(f'\n[orange]fastboot is not installed, downloading...\n[/orange]')
        return download_platform_tools()

    except Exception as e:
        console.print(f"[red]✗ Error checking fastboot: {str(e)}[/red]")
        raise SystemExit(1)
