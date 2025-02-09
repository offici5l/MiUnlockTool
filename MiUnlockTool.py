#!/usr/bin/python

version = "dev-1.5.9"

print(f"\n[V{version}]\nhttps://github.com/offici5l/MiUnlockTool")

import os

for lib in ['Cryptodome', 'requests']:
    try: __import__(lib)
    except ImportError:
        p = os.getenv("PREFIX", "")
        cmd = ('pkg install python-pycryptodomex' if "com.termux" in p 
               else f'pip install pycryptodomex') if lib == 'Cryptodome' else f'pip install {lib}'
        os.system(cmd)

import requests, json, hashlib, urllib.parse, time, shelve, sys, binascii, hmac, re, random
from base64 import b64encode, b64decode
from urllib.parse import urlparse, urlencode, parse_qs, quote_plus
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import base64

headers = {"User-Agent": "offici5l/MiUnlockTool"}

def login():

    user = input('\nEnter user: ')
    pwd = input('\nEnter pwd: ')

    opts = {"1": {"chk": "Address", "v": "Email"}, "2": {"chk": "Phone", "v": "Phone"}}

    choice = input("\nAccount verification\n\n1 Email address\n2 Phone number (requires solving CAPTCHA)\n\nChoose a verification method: ")
    if choice not in opts: exit("Invalid choice.")

    opt = opts[choice]
    
    base = "https://account.xiaomi.com"
    Auth = base + "/pass/serviceLogin"
    Auth2 = Auth + "Auth2"
    urlsv = base + "/identity/auth/"
    urlsend = urlsv + "send" + opt["v"] + "Ticket"
    urlverify = urlsv + "verify" + opt["v"]  
    url = Auth + "?sid=unlockApi&checkSafe" + opt["chk"] + "=true"


    try:
        r = requests.get(url, headers=headers)
        cookies = r.cookies.get_dict()
    except Exception as e:
        exit(f"r: {type(e).__name__}")

    data = {
        "_json": "true",
        "callback": "https://unlock.update.miui.com/sts",
        "sid": "unlockApi",
        "qs": re.search(r"qs\s*:\s*'([^']+)'", r.text).group(1),
        "_sign": re.search(r'"_sign"\s*:\s*"([^"]+)"', r.text).group(1),
        "serviceParam": re.search(r"serviceParam\s*:\s*'([^']+)'", r.text).group(1),
        "user": user,
        "hash": hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest().upper(),
        "_locale": "en_US",
        "useManMachine": "false"
    }

    try:
        r1 = requests.post(Auth2, data=data, headers=headers, cookies=cookies)
        r1_text = json.loads(r1.text[11:])
        if r1_text["code"] == 70016: exit("invalid user or pwd")
        notificationUrl = r1_text.get("notificationUrl") or exit("r1: notificationUrl not found")
        if "BindAppealOrSafePhone" in notificationUrl or "SetEmail" in notificationUrl:
            exit(notificationUrl)
        cookies.update(requests.get(notificationUrl, headers=headers, cookies=cookies).cookies.get_dict())
    except Exception as e:
        exit(f"r1: {type(e).__name__}")
    

    try:
        data_icode = {}
        while True:
            r2 = requests.post(urlsend, data=data_icode, cookies=cookies, headers=headers)
            r2_text = json.loads(r2.text[11:])
            if r2_text["code"] == 87001:
                print(r2_text["reason"])
                path = "/sdcard/captcha.jpg" if os.path.exists("/sdcard") else "captcha.jpg"
                rc = requests.get(f"{base}/pass/getCode?icodeType=login", cookies=cookies)
                cookies.update(rc.cookies.get_dict())
                with open(path, "wb") as f:
                    f.write(rc.content)
                print(f"\nCaptcha saved as {path}")
                icode = input("\nEnter captcha code: ").strip()
                data_icode.update({'icode': icode})
            elif r2_text["code"] == 0:
                print(f"\nVerification code sent to your {opt["v"]}")
                break
            else:
                exit(r2_text["tips"] if r2_text["code"] == 70022 else r2_text)
    except Exception as e:
        exit(f"r2: {type(e).__name__}")

    while True:
        ticket = input("Enter code: ").strip()
        try:
            r3 = requests.post(urlverify, data={'ticket': ticket, 'trust': 'true'}, headers=headers, cookies=cookies)
            r3_text = json.loads(r3.text[11:])
            if r3_text["code"] == 70014:
                print(r3_text["tips"])
                continue
            elif r3_text["code"] == 0:
                break
            else:
                exit(r3_text)
        except Exception as e:
            exit(f"r3: {type(e).__name__}")


    try:
        r4 = requests.post(Auth2, data=data, headers=headers, cookies=cookies).cookies.get_dict()
        del r4['cUserId'], r4['passInfo'], r4['uLocale']
    except Exception as e:
        exit(f"r4: {type(e).__name__}")

    try:
        r5 = json.loads(requests.get(f"{base}/pass/user/login/region", headers=headers, cookies=r4).text[11:])["data"]["region"]
    except Exception as e:
        exit(f"r5: {type(e).__name__}")

    try:
        r6 = next(k for k, v in json.loads(requests.get(f"{base}/pass2/config?key=regionConfig").text[11:])["regionConfig"].items() if v.get("region.codes") and r5 in v["region.codes"])
    except Exception as e:
        exit(f"r6: {type(e).__name__}")

    midata = {"cookies": r4, "url": url, "region": r5, 'regionConfig': r6}
    with open("midata.json", "w") as f:
        json.dump(midata, f, indent=4)

    return midata


try:
    with open('midata.json', 'r') as f:
        midata = json.load(f)
    print(f"\nAccount ID: {midata["cookies"]["userId"]}")
    input(f"Press 'Enter' to continue.\nPress 'Ctrl' + 'd' to log out.")
except (FileNotFoundError, json.JSONDecodeError, EOFError):
    if os.path.exists('midata.json'):
        os.remove('midata.json')
    midata = login()


cookies = midata["cookies"]
url = midata["url"]
pcId = hashlib.md5(midata["cookies"]["deviceId"].encode()).hexdigest()
region = midata["region"]
regionConfig = midata["regionConfig"]

print(f"\nAccount Region: {region}")

try:
    r8 = requests.get(url, cookies=cookies, headers=headers)
    ssecurity = json.loads(r8.history[0].headers['extension-pragma'])['ssecurity']
    cookies = r8.cookies.get_dict()
    if not cookies: raise ValueError("Cookies are empty")
except (Exception, KeyError, ValueError) as e:
    exit(f"r8: {type(e).__name__} - {str(e)}")

Subdomains = {"Singapore": "unlock.update.intl", "China": "unlock.update", "India": "in-unlock.update.intl", "Russia": "ru-unlock.update.intl", "Europe": "eu-unlock.update.intl"}

try:
    input(f"\nregionConfig: {regionConfig}\nPress 'Enter' to continue\npress 'Ctrl' + 'd' to select it manually.\n")
    Subdomain = Subdomains[regionConfig]
except (EOFError):
    for idx, name in enumerate(Subdomains, 1):
        print(f"\n{idx}: {name}")
    selection = input("\nregionConfig: ").strip()
    Subdomain = list(Subdomains.values())[int(selection) - 1] if selection.isdigit() and 1 <= int(selection) <= len(Subdomains) else exit("Invalid selection")


session = requests.Session()

def send(path, param_order, params_raw):

    if 'data' in params_raw:
        params_raw['data'] = json.dumps(params_raw['data'])
        params_raw['data'] = b64encode(params_raw['data'].encode()).decode()

    cipher = lambda: AES.new(b64decode(ssecurity), AES.MODE_CBC, b'0102030405060708')

    ep = lambda ep: b64encode(cipher().encrypt(pad(ep.encode(), AES.block_size))).decode()

    params_raw["sid"] = 'miui_unlocktool_client'
    sign_params = '&'.join([f"{k}={params_raw[k]}" for k in param_order])
    sign_str = f"POST\n{path}\n{sign_params}"
    current_sign = b64encode(cipher().encrypt(pad(binascii.hexlify(hmac.new(b'2tBeoEyJTunmWUGq7bQH2Abn0k2NhhurOaqBfyxCuLVgn4AVj7swcawe53uDUno', sign_str.encode(), hashlib.sha1).digest()).decode().encode(), AES.block_size))).decode()
    
    encoded_params = [f"{k}={ep(params_raw[k])}" for k in param_order]
    encoded_params.extend([f"sign={current_sign}", ssecurity])
    sha1_input = f"POST&{path}&{'&'.join(encoded_params)}"
    signature = b64encode(hashlib.sha1(sha1_input.encode()).digest()).decode()
    
    post_params = {k: ep(params_raw[k]) for k in param_order}
    post_params.update({'sign': current_sign, 'signature': signature})
    
    try:
        r9 = session.post("https://" + Subdomain + ".miui.com" + path, params=post_params, cookies=cookies, headers=headers)
    except Exception as e:
        exit(f"r9: {type(e).__name__}")

    dresponse = json.loads(b64decode(unpad(cipher().decrypt(b64decode(r9.text)), AES.block_size)).decode())

    return dresponse


try:
    token = input("python fastboot.py getvar token\nor\npython fastboot.py oem get_token\n\nNote:\nIf you have token1 and token2,\nenter them as: token1token2\n\nEnter the device token: """)
    token += '=' * (-len(token) % 4)
    decoded = base64.urlsafe_b64decode(token)
    if len(decoded) < 32:
        raise ValueError("Token length mismatch")
    product = decoded[24:30].decode('ascii', errors='strict')
    cpuid = f"0x{int.from_bytes(decoded[32:], 'big'):08x}"    
except (ValueError, UnicodeDecodeError) as e:
    exit(e)

print(f"\nproduct: {product} | cpuid: {cpuid}\n")

nr = send('/api/v2/nonce', ['r', 'sid'], {'r': ''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16))})
nonce = nr.get('nonce')
if not nonce: exit(nr)

cr = send('/api/v2/unlock/device/clear', ['data', 'nonce', 'sid'], {'data': {"product": product}, 'nonce': nonce})
try:
    print("\n".join([f"{key}: {value}" for key, value in cr.items()]))
    input("\nPress 'Enter' to get encryptData\nPress 'Ctrl' + 'd' to exit\n")
except EOFError:
    exit()

ar = send('/api/v3/ahaUnlock', ['appId', 'data', 'nonce', 'sid'], {'appId': '1', 'data': {"clientId": "2", "clientVersion": "7.6.727.43", "deviceInfo": {"boardVersion": "", "deviceName": "", "product": product, "socId": ""}, "deviceToken": token, "language": "en", "operate": "unlock", "pcId": pcId, "region": "", "uid": midata["cookies"]["userId"]}, 'nonce': nonce})

print("\n".join([f"{key}: {value}" for key, value in ar.items()]))
    
if "code" in ar and ar["code"] == 0:
    encryptData = ar["encryptData"]
    print(f"\n\nUse one of the following commands to unlock the bootloader:\n\nfastboot oem unlock {encryptData}\n\nor\n\nfastboot flashing unlock {encryptData}\n")