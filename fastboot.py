#!/usr/bin/python  

import os

try:
    __import__("usb")
except ImportError:
    os.system("pip install pyusb -q")

import usb.core, usb.util, sys, subprocess, time, shutil, json

if len(sys.argv) < 2:
    exit("\nhttps://github.com/offici5l/MiUnlockTool\n\nUsage: python fastboot.py <command>\n")  

def handle_termux():  
    if '/data/data/com.termux' in __file__: 
        if subprocess.run(['su', '-c', 'id'], capture_output=True).returncode == 0:  
            if "SUDO_USER" not in os.environ:
                if not shutil.which('tsu'):
                    os.system("apt-get download tsu >/dev/null 2>&1 && dpkg -i tsu_*_all.deb >/dev/null 2>&1")  
                os.execvp('sudo', ['sudo', sys.executable, __file__] + sys.argv[1:])  
        else:  
            if "TERMUX_USB_FD" not in os.environ or json.loads(subprocess.run(["termux-usb", "-l"], capture_output=True, text=True).stdout.strip()) == []:  
                if not shutil.which('termux-usb'):  
                    os.system("apt-get download termux-api >/dev/null 2>&1 && dpkg -i termux-api_*.deb >/dev/null 2>&1")  
                if not os.path.exists("/data/data/com.termux.api"):  
                    exit("\ntermux.api app is not installed\n")  
                while True:  
                    device = "\n".join(subprocess.run(['termux-usb', '-l'], capture_output=True, text=True).stdout.replace('[', '').replace(']', '').replace('"', '').split())  
                    if device:  
                        if 'Access granted.' in subprocess.run(['termux-usb', '-r', device], capture_output=True, text=True).stdout:  
                            cmd = f"{sys.executable} {__file__} {' '.join(sys.argv[1:])}"  
                            os.execvp('termux-usb', ['termux-usb', '-E', '-e', cmd, '-r', device])  
                    else:  
                        print("\rwaiting for device", end="", flush=True); time.sleep(2); print("\r\033[K", end="", flush=True)


def find_fastboot_device():
    handle_termux()
    try:
        devices = usb.core.find(find_all=True)
    except Exception as e:
        return None, e

    device = out_ep = in_ep = out_max = in_max = None

    for dev in devices:
        for cfg in dev:
            for intf in cfg:
                if (intf.bInterfaceClass == 0xff and intf.bInterfaceSubClass == 0x42 and intf.bInterfaceProtocol == 0x03):
                    for ep in intf:
                        ep_dir = usb.util.endpoint_direction(ep.bEndpointAddress)
                        if ep_dir == usb.util.ENDPOINT_OUT:
                            out_ep = ep.bEndpointAddress
                            out_max = ep.wMaxPacketSize
                        elif ep_dir == usb.util.ENDPOINT_IN:
                            in_ep = ep.bEndpointAddress
                            in_max = ep.wMaxPacketSize
                    if not out_ep or not in_ep:
                        continue
                    if dev.is_kernel_driver_active(intf.bInterfaceNumber):
                        dev.detach_kernel_driver(intf.bInterfaceNumber)
                        dev.set_configuration(cfg.bConfigurationValue)
                        usb.util.claim_interface(dev, intf.bInterfaceNumber)
                    device = dev
                    break
            if device:
                break
        if device:
            break

    return device, (out_ep, in_ep, out_max, in_max)

device, endpoints = find_fastboot_device()
if not device:
    print("\rwaiting for device", end="", flush=True); time.sleep(2); print("\r\033[K", end="", flush=True)
    os.execvp(__file__, [__file__] + sys.argv[1:])

out_ep, in_ep, out_max, in_max = endpoints  

try:  
    cmd = ' '.join(sys.argv[1:]).encode()  
    for offset in range(0, len(cmd), out_max):  
        device.write(out_ep, cmd[offset:offset+out_max], 14000)  
    while True:  
        resp = bytes(device.read(in_ep, in_max, 14000)).decode()          
        if len(resp) < 4:  
            print(resp)  
            break              
        prfx, data = resp[:4], resp[4:]  
        print(f"{prfx}: {data}" if data else prfx)      
        if prfx != 'INFO':  
            break  
except Exception as e:  
    exit(e)