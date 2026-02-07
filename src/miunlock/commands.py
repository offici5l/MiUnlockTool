import subprocess
import threading
import time

from migate.config import (
    console
)

def read_stream(stream, output_list, process, restart_flag, status):
    try:
        for line in iter(stream.readline, ''):
            line = line.strip()
            output_list.append(line)
            if "No permission" in line or "< waiting for any device >" in line:
                process.terminate()
                status.update(f'[orange]< waiting for any device >[/orange]')
                restart_flag[0] = True
                return
    finally:
        stream.close()

def CheckB(cmd, var_name, *fastboot_args):

    with console.status("[white]Initializing...[/white]") as status:

        while True:

            try:
                process = subprocess.Popen(
                    [cmd] + list(fastboot_args),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=1,
                    universal_newlines=True
                )

            except FileNotFoundError:
                return {'error': f"Fastboot command '{cmd}' not found in PATH"}

            except PermissionError:
                return {'error': 'Permission denied. Run PowerShell as Administrator'}

            except Exception as e:
                return {'error': f"{type(e).__name__}: {str(e)}"}


            stdout_lines, stderr_lines, restart_flag = [], [], [False]

            threading.Thread(
                target=read_stream,
                args=(process.stdout, stdout_lines, process, restart_flag, status),
                daemon=True
            ).start()

            threading.Thread(
                target=read_stream,
                args=(process.stderr, stderr_lines, process, restart_flag, status),
                daemon=True
            ).start()

            try:
                process.wait()
            except subprocess.SubprocessError as e:
                console.print(f"\n[red]Error while executing process: {e}[/red]\n")
                return None

            if restart_flag[0]:
                time.sleep(2)
                continue

            status.update(f"[white]Fetching '{var_name}' — please wait...[/white]")
            break


        lines = [
            line.split(f"{var_name}:")[1].strip()
            for line in stderr_lines + stdout_lines
            if f"{var_name}:" in line
        ]

        if len(lines) > 1:
            return "".join(lines)
        return lines[0] if lines else None

def get_product(cmd):
    product = None
    while product is None:
        product = CheckB(cmd, "product", "getvar", "product")
        if isinstance(product, dict) and 'error' in product:
            return product
    console.print(f"\n[green]product: {product}[/green]\n")
    return product

def get_device_token(cmd):
    token = None
    while token is None:
        token = CheckB(cmd, "token", "oem", "get_token")
        if isinstance(token, dict) and 'error' in token:
            return token
        if token:
            console.print(f"\n[green]device token: {token}[/green]\n")
            return token
        else:
            token = CheckB(cmd, "token", "getvar", "token")
            if isinstance(token, dict) and 'error' in token:
                return token
            if token:
                console.print(f"\n[green]device token: {token}[/green]\n")
                return token