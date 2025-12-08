import time
import json
import platform
import requests
import subprocess
from pathlib import Path

headers = {"User-Agent": "XiaomiPCSuite"}

def download_captcha(path, captchaUrl, cookies):    
    response = requests.get(f"https://account.xiaomi.com{captchaUrl}", cookies=cookies, headers=headers)
    cookies.update(response.cookies.get_dict())
    with open(path, "wb") as f:
        f.write(response.content)
    input('\nPress Enter to open the CAPTCHA image')
    if platform.system() == 'Windows':
        subprocess.run(['start', str(path)], shell=True)
    elif platform.system() == 'Darwin':
        subprocess.run(['open', str(path)])
    else:
        subprocess.run(['xdg-open', str(path)])
    
    print(f"\nCaptcha displayed from {path}")
    return cookies

def verify(captchaUrl, cookies, data):
    path = Path.home() / f"{int(time.time())}_captcha.jpg"
    cookies = download_captcha(path, captchaUrl, cookies)
    captCode = input("\nEnter captcha code: ").strip()
    data.update({'captCode': captCode})
    response = requests.post(f"https://account.xiaomi.com/pass/serviceLoginAuth2", data=data, headers=headers, cookies=cookies)
    response_text = json.loads(response.text[11:])
    if response_text.get("code") == 87001:
        path.unlink()
        print("\nIncorrect captcha code. A new captcha will be generated ...")
        return verify(response_text["captchaUrl"], response.cookies.get_dict(), data)
    cookies = response.cookies.get_dict()
    path.unlink()

    return cookies