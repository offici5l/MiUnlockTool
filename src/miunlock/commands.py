import subprocess
import threading
import time
import sys

def read_stream(stream, output_list, process, restart_flag):
    try:
        for line in iter(stream.readline, ''):
            line = line.strip()
            output_list.append(line)
            if "No permission" in line or "< waiting for any device >" in line:
                process.terminate()
                print(f'\r< waiting for any device >', end='', flush=True)
                restart_flag[0] = True
                return
    finally:
        stream.close()

def CheckB(cmd, var_name, *fastboot_args):
    while True:
        process = subprocess.Popen([cmd] + list(fastboot_args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        stdout_lines, stderr_lines, restart_flag = [], [], [False]

        threading.Thread(target=read_stream, args=(process.stdout, stdout_lines, process, restart_flag)).start()
        threading.Thread(target=read_stream, args=(process.stderr, stderr_lines, process, restart_flag)).start()

        try:
            process.wait()
        except subprocess.SubprocessError as e:
            print(f"\nError while executing process: {e}")
            return None

        if restart_flag[0]:
            time.sleep(2)
            sys.stdout.write('\r\033[K')
            continue

        print(f"\rFetching '{var_name}' — please wait...", end='', flush=True)

        lines = [line.split(f"{var_name}:")[1].strip() for line in stderr_lines + stdout_lines if f"{var_name}:" in line]
        if len(lines) > 1:
            return "".join(lines)
        return lines[0] if lines else None

def get_product(cmd):
    product = None
    while product is None:
        if product is None:
            product = CheckB(cmd, "product", "getvar", "product")
    print(f"\nproduct: {product}\n")
    return product


def get_device_token(cmd):
    token = None
    while token is None:
        if token is None:
            token = CheckB(cmd, "token", "oem", "get_token")
            if token:
                print(f"\ndevice token: {token}")
                return token
            else:
                token = CheckB(cmd, "token", "getvar", "token")
                if token:
                    print(f"\ndevice token: {token}")
                    return token