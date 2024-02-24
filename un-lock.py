#!/usr/bin/python

version = "1.5.0"
cv = {"clientVersion": "6.5.224.28"}
notice = f"\n\033[2m(version: {version}) for Report issues or share feedback at:\ngithub.com/offici5l/un-lock/issues t.me/Offici5l_Group\033[0m\n"
p_ = "\n\033[32m" + "_"*56 + "\033[0m\n"

import os

for lib in ['Cryptodome', 'urllib3', 'requests']:
    try:
        __import__(lib)
    except ImportError:
        print(f"\nInstalling {lib}...\n")
        os.system('yes | pkg update' if "com.termux" in os.getenv("PREFIX", "") else '')
        os.system(f'pip install pycryptodomex' if lib == 'Cryptodome' else f'pip install {lib}')

import re, requests, json, hmac, random, binascii, urllib, hashlib, io, urllib.parse, time, sys, urllib.request, zipfile, webbrowser, platform, subprocess, shutil
from urllib3.util.url import Url
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from urllib.parse import urlparse, parse_qs, urlencode

def dw(s):
    print("\ndownload platform-tools...\n")
    url = f"https://dl.google.com/android/repository/platform-tools-latest-{s}.zip"
    cd = os.path.join(os.path.dirname(__file__))
    fp = os.path.join(cd, os.path.basename(url))    
    urllib.request.urlretrieve(url, fp)    
    with zipfile.ZipFile(fp, 'r') as zip_ref:
        zip_ref.extractall(cd)   
    os.remove(fp)


def dwt():
    os.system("yes | pkg uninstall termux-adb; curl -s https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh | bash; ln -s $PREFIX/bin/termux-fastboot $PREFIX/bin/tfastboot")
    print(notice)
    print("\nSetup completed successfully!\nTo use un-lock, run the command: \033[92munlock\033[0m\n")
    exit()

s = platform.system()
if s == "Linux" and os.path.exists("/data/data/com.termux"):
    try:
        result = os.popen("tfastboot --version").read()
        if "fastboot version" not in result:
            dwt()
    except (FileNotFoundError, Exception):
        dwt()
    up = os.path.join(os.getenv("PREFIX", ""), "bin", "unlock")
    if not os.path.exists(up):
        shutil.copy(__file__, up)
        os.system(f"chmod +x {up}")
    cmd = "tfastboot"
    datafile = "/sdcard/Download/data.json"
    browserp = "t"
else:
    dir = os.path.dirname(__file__)
    fp = os.path.join(dir, "platform-tools")
    if not os.path.exists(fp):
        dw(s)
    cmd = os.path.join(fp, "fastboot")
    datafile = os.path.join(dir, "data.json")
    browserp = "wlm"

while os.path.isfile(datafile):
    try:
        with open(datafile, "r") as file:
            data = json.load(file)
        if len(sys.argv) > 1 and sys.argv[1] == "1":
            choice = "1"
            break
        elif data:
            choice = input(f"\nPrevious Data Exists! in {datafile}\n\n\n- \033[92m1\033[0m Use Previous Data\n- \033[92m2\033[0m Delete Previous Data\n\n\nEnter your \033[92mchoice\033[0m: ").lower()
            if choice == "1":
                break
            elif choice == "2":
                os.remove(datafile)
                break
            else:
                print("\nInvalid choice. Enter '1' or '2'.")
        else:
            os.remove(datafile)
            break
    except json.JSONDecodeError:
        os.remove(datafile)

def remove(*keys):
    print(f"\ninvalid {keys[0] if len(keys) == 1 else ' or '.join(keys)}\n")
    with open(datafile, "r+") as file:
        data = json.load(file)
        for key in keys:
            data.pop(key, None)
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()
    subprocess.run(["python", __file__, "1"])

def CheckB(cmd):
    print("\nCheck if the device is connected via OTG in bootloader mode...\n")
    while True:
        try:
            result = subprocess.run([cmd, "getvar", "all"], capture_output=True, text=True, timeout=1)
        except subprocess.TimeoutExpired:
            continue
        lines = [line.split(":")[1].strip() for line in result.stderr.split('\n') if "token" in line or "product" in line]
        return {"product": lines[1], "deviceToken": lines[0]} if len(lines) == 2 else None


try:
    with open(datafile, "r+") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}
    with open(datafile, 'w') as file:
        json.dump(data, file)
for key in ["user", "pwd", "wb_id", "deviceToken", "product"]:
    if key not in data:
        if key == "user":
            data[key] = input("\n(Xiaomi Account) Id or Email or Phone: ")
        elif key == "pwd":
            data[key] = hashlib.md5(input("Enter password: ").encode()).hexdigest().upper()
        elif key == "wb_id":
            input("\nPress Enter to open confirmation page, copy link after seeing {\"R\":\"\",\"S\":\"OK\"}, and return here")
            conl = 'https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true&passive=false&hidden=false'
            if browserp == "t":
                os.system(f"termux-open-url '{conl}'")
            elif browserp == "wlm":
                webbrowser.open(conl)
            wb_id = parse_qs(urlparse(input("\nEnter Link: ")).query).get('d', [None])[0]
            if wb_id is None:
                print("\n\nInvalid link\n")
                subprocess.run(["python", __file__, "1"])
                sys.exit()
            data[key] = wb_id
        elif key in ["deviceToken", "product"]:
            tp = CheckB(cmd)
            if tp is not None:
                data[key] = tp[key]
            else:
                data["deviceToken"] = input("Enter deviceToken: ")
                data["product"] = input("Enter product: ")
        print(f"\n{key} saved.\n")
        with open(datafile, "r+") as file:
            json.dump(data, file, indent=2)
user, pwd, wb_id, product, deviceToken = (data.get(key, "") for key in ["user", "pwd", "wb_id", "product", "deviceToken"])

session = requests.Session()
headers = {"User-Agent": "XiaomiPCSuite"}

def postv(sid):
    return json.loads(session.post(f"https://account.xiaomi.com/pass/serviceLoginAuth2?sid={sid}&_json=true&passive=true&hidden=true", data={"user": user, "hash": pwd}, headers=headers, cookies={"deviceId": str(wb_id)}).text.replace("&&&START&&&", ""))

data = postv("unlockApi")

if data["code"] == 70016:
    print("\n\nincorrect Id/Email/Phone or password\n\n")
    remove("user", "pwd")
    sys.exit()

if data["securityStatus"] == 16:
    p = postv("passport")
    data = json.loads(requests.get("https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&_json=true&passive=true&hidden=true", headers=headers, cookies={'passToken': p['passToken'], 'userId': str(p['userId']), 'deviceId': parse_qs(urlparse(p['location']).query)['d'][0]}).text.replace("&&&START&&&", ""))

ssecurity, nonce, location = data["ssecurity"], data["nonce"], data["location"]

rc = session.get(location + "&clientSign=" + urllib.parse.quote_plus(b64encode(hashlib.sha1(f"nonce={nonce}".encode("utf-8") + b"&" + ssecurity.encode("utf-8")).digest())), headers=headers)

cookies = {cookie.name: cookie.value for cookie in rc.cookies}

if 'serviceToken' not in cookies:
    print("\nFailed to get serviceToken.")
    remove("wb_id")
    sys.exit()

url = {"india": "https://in-unlock.update.intl.miui.com", "global": "https://unlock.update.intl.miui.com", "china": "https://unlock.update.miui.com", "russia": "https://ru-unlock.update.intl.miui.com", "europe": "https://eu-unlock.update.intl.miui.com"}.get(parse_qs(urlparse(rc.url).query).get('p_idc', [None])[0].lower() if parse_qs(urlparse(rc.url).query).get('p_idc', [None])[0].lower() in ['india', 'europe', 'russia', 'china'] else 'global', '')

class RetrieveEncryptData:
    def add_nonce(self):
        r = RetrieveEncryptData("/api/v2/nonce", {"r":''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid":"miui_unlocktool_client"}).run()
        self.params[b"nonce"] = r["nonce"].encode("utf-8")
        self.params[b"sid"] = b"miui_unlocktool_client"
        return self
    def __init__(self, path, params):
        self.path = path
        self.params = {k.encode("utf-8"): v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in params.items()}
    def get_params(self, sep):
        return b'POST'+sep+self.path.encode("utf-8")+sep+b"&".join([k+b"="+v for k,v in self.params.items()])
    def add_sign(self):
        self.params[b"sign"] = binascii.hexlify(hmac.digest(b'2tBeoEyJTunmWUGq7bQH2Abn0k2NhhurOaqBfyxCuLVgn4AVj7swcawe53uDUno', self.get_params(b"\n"), "sha1"))
    def encrypt_params(self):
        for k, v in self.params.items():
            self.params[k] = b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt(v + (16 - len(v) % 16) * bytes([16 - len(v) % 16])))
    def add_signature(self):
        self.params[b"signature"] = b64encode(hashlib.sha1(self.get_params(b"&")+b"&"+ssecurity.encode("utf-8")).digest())
    def run(self):
        self.add_sign()
        self.encrypt_params()
        self.add_signature()
        return json.loads(b64decode((lambda s: s[:-s[-1]])(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(b64decode(session.post(Url(host=url, path=self.path).url, data=self.params, headers=headers, cookies=cookies).text)))))

path_data = {"/api/v3/unlock/userinfo": {"data": cv}, "/api/v2/unlock/device/clear": {"data": {**cv, "product": product}}, "/api/v3/ahaUnlock": {"data": {**cv, "deviceInfo": {"product": product}, "deviceToken": deviceToken}}}

print(p_)
for path, data in path_data.items():
    r = RetrieveEncryptData(path, data).add_nonce().run()
    for key, value in r.items():
        print(f"\n{key}: {value}")
    print(p_)
    if "encryptData" in r:
        ed = io.BytesIO(bytes.fromhex(r["encryptData"]))
        with open("encryptData", "wb") as edfile:
            edfile.write(ed.getvalue())
        CheckB(cmd)
        os.system(f"{cmd} stage encryptData")
        os.system(f"{cmd} oem unlock")
    if "code" in r and r["code"] == 10000:
        remove("product", "deviceToken")
        sys.exit()

print(notice)
browserp == "wlm" and input("\nPress Enter to exit ...")