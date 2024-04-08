#!/usr/bin/python

version = "1.5.0"
notice = f"\033[2m(version: {version}) For issues or feedback:\n- GitHub: github.com/offici5l/MiUnlockTool/issues\n- Telegram: t.me/Offici5l_Group\033[0m\n"
p_ = "\n\033[32m" + "_"*56 + "\033[0m\n"

import os

for lib in ['Cryptodome', 'urllib3', 'requests']:
    try:
        __import__(lib)
    except ImportError:
        print(f"\nInstalling {lib}...\n")
        os.system('yes | pkg update' if "com.termux" in os.getenv("PREFIX", "") else '')
        os.system(f'pip install pycryptodomex' if lib == 'Cryptodome' else f'pip install {lib}')

import re, requests, json, hmac, random, binascii, urllib, hashlib, io, urllib.parse, time, sys, urllib.request, zipfile, webbrowser, platform, subprocess, shutil, stat
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
    print(notice)

up = os.path.join(os.getenv("PREFIX", ""), "bin", "miunlock")
ttp = "\nuse command: \033[92mmiunlock\033[0m\n"

def dwt():
    os.system("yes | pkg uninstall termux-adb 2>/dev/null; curl -s https://raw.githubusercontent.com/nohajc/termux-adb/master/install.sh | bash; ln -s $PREFIX/bin/termux-fastboot $PREFIX/bin/fastboot")
    print(notice)
    if os.path.exists(up):
        print(ttp)
        exit()

s = platform.system()
if s == "Linux" and os.path.exists("/data/data/com.termux"):
    try:
        result_fastboot = os.popen("fastboot --version").read()
        if "fastboot version" not in result_fastboot:
            dwt()
    except (FileNotFoundError, Exception):
        dwt()
    if not os.path.exists(up):
        shutil.copy(__file__, up)
        os.system(f"chmod +x {up}")
        print(ttp)
        exit()
    if not os.path.exists("/data/data/com.termux.api"):
        print("\nThe com.termux.api application is not installed on the device. Please install it first : \n\nhttps://github.com/termux/termux-api/releases/download/v0.50.1/termux-api_v0.50.1+github-debug.apk")
        exit()
    cmd = "fastboot"
    datafile = "/sdcard/Download/data.json"
    browserp = "t"
else:
    dir = os.path.dirname(__file__)
    fp = os.path.join(dir, "platform-tools")
    if not os.path.exists(fp):
        dw(s)
    cmd = os.path.join(fp, "fastboot")
    if s == "Linux" or s == "Darwin":
        st = os.stat(cmd)
        os.chmod(cmd, st.st_mode | stat.S_IEXEC)
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
    print(f"\n\033[91minvalid {keys[0] if len(keys) == 1 else ' or '.join(keys)}\033[0m\n")
    with open(datafile, "r+") as file:
        data = json.load(file)
        for key in keys:
            data.pop(key, None)
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()
    subprocess.run(["python", __file__, "1"])

def CheckB(cmd, var_name, *fastboot_args):
    print(f"\nCheck if device is connected in bootloader mode...\n")
    while True:
        try:
            result = subprocess.run([cmd] + list(fastboot_args), capture_output=True, text=True, timeout=1)
        except subprocess.TimeoutExpired:
            continue     
        lines = [line.split(f"{var_name}:")[1].strip() for line in result.stderr.split('\n') if f"{var_name}:" in line]
        if len(lines) > 1:
            cvalue = "".join(lines)
            return cvalue       
        return lines[0] if lines else None

try:
    with open(datafile, "r+") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}
    with open(datafile, 'w') as file:
        json.dump(data, file)

def save(data, path, name=None):
    with open(path, "w") as file:
        json.dump(data, file, indent=2)
    if name:
        print(f"\n\033[92m{name} saved successfully\033[0m\n")

if "user" not in data:
    data["user"] = input("\n(Xiaomi Account) Id or Email or Phone: ")
    save(data, datafile, name="user")

if "pwd" not in data:
    data["pwd"] = input("Enter password: ")
    save(data, datafile, name="pwd")

if "wb_id" not in data:
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
    data["wb_id"] = wb_id
    save(data, datafile, name="wb_id")

if "product" not in data:
    p = CheckB(cmd, "product", "getvar", "product")
    if not p:
        p = input("\nFailed to obtain the deviceProduct. Please enter it manually: ")
    data["product"] = p
    save(data, datafile, name="product")

if "token" not in data:
    t = CheckB(cmd, "token", "oem", "get_token")
    if not t:
        t = CheckB(cmd, "token", "getvar", "token")
        if not t:
            t = input("\nFailed to obtain the deviceToken !\n Please enter it manually: ")
    data["token"] = t
    save(data, datafile, name="token")

user, pwd, wb_id, product, token = (data.get(key, "") for key in ["user", "pwd", "wb_id", "product", "token"])

print(f"\nDeviceInfo:\nproduct: \033[92m{product}\033[0m\ntoken: \033[92m{token}\033[0m\n")

session = requests.Session()
headers = {"User-Agent": "XiaomiPCSuite"}

def postv(sid):
    return json.loads(session.post(f"https://account.xiaomi.com/pass/serviceLoginAuth2?sid={sid}&_json=true&passive=true&hidden=true", data={"user": user, "hash": hashlib.md5(pwd.encode()).hexdigest().upper()}, headers=headers, cookies={"deviceId": str(wb_id)}).text.replace("&&&START&&&", ""))

data = postv("unlockApi")

if data["code"] == 70016:
    remove("user", "pwd")
    sys.exit()

if data["securityStatus"] == 16:
    p = postv("passport")
    data = json.loads(requests.get("https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&_json=true&passive=true&hidden=true", headers=headers, cookies={'passToken': p['passToken'], 'userId': str(p['userId']), 'deviceId': parse_qs(urlparse(p['location']).query)['d'][0]}).text.replace("&&&START&&&", ""))

ssecurity, nonce, location = data["ssecurity"], data["nonce"], data["location"]

cookies = {cookie.name: cookie.value for cookie in session.get(location + "&clientSign=" + urllib.parse.quote_plus(b64encode(hashlib.sha1(f"nonce={nonce}".encode("utf-8") + b"&" + ssecurity.encode("utf-8")).digest())), headers=headers).cookies}

if 'serviceToken' not in cookies:
    print("\nFailed to get serviceToken.")
    remove("wb_id")
    sys.exit()

region = parse_qs(urlparse(location).query).get('p_idc', [''])[0].lower()
g = "unlock.update.intl.miui.com"
url = {'china': g.replace("intl.", ""), 'india': f"in-{g}", 'russia': f"ru-{g}", 'europe': f"eu-{g}"}.get(region, g)

print(f"AccountInfo:\nid: \033[92m{data['userId']}\033[0m\nregion: \033[92m{region}\033[0m")

class RetrieveEncryptData:
    def add_nonce(self):
        r = RetrieveEncryptData("/api/v2/nonce", {"r":''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid":"miui_unlocktool_client"}).run()
        self.params[b"nonce"] = r["nonce"].encode("utf-8")
        self.params[b"sid"] = b"miui_unlocktool_client"
        return self
    def __init__(self, path, params):
        self.path = path
        self.params = {k.encode("utf-8"): v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in params.items()}
    def getp(self, sep):
        return b'POST'+sep+self.path.encode("utf-8")+sep+b"&".join([k+b"="+v for k,v in self.params.items()])
    def run(self):
        self.params[b"sign"] = binascii.hexlify(hmac.digest(b'2tBeoEyJTunmWUGq7bQH2Abn0k2NhhurOaqBfyxCuLVgn4AVj7swcawe53uDUno', self.getp(b"\n"), "sha1"))
        for k, v in self.params.items():
            self.params[k] = b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt(v + (16 - len(v) % 16) * bytes([16 - len(v) % 16])))
        self.params[b"signature"] = b64encode(hashlib.sha1(self.getp(b"&")+b"&"+ssecurity.encode("utf-8")).digest())
        return json.loads(b64decode((lambda s: s[:-s[-1]])(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(b64decode(session.post(Url(scheme="https", host=url, path=self.path).url, data=self.params, headers=headers, cookies=cookies).text)))))

print(p_)

r = RetrieveEncryptData("/api/v3/ahaUnlock", {"appId":"1", "data":{"clientId":"2", "clientVersion":"7.6.727.43", "language":"en", "operate":"unlock", "pcId":hashlib.md5(wb_id.encode("utf-8")).hexdigest(), "product":product, "region":"","deviceInfo":{"boardVersion":"","product":product, "socId":"","deviceName":""}, "deviceToken":token}}).add_nonce().run()

if "code" in r and r["code"] == 0:
    ed = io.BytesIO(bytes.fromhex(r["encryptData"]))
    with open("encryptData", "wb") as edfile:
        edfile.write(ed.getvalue())
    CheckB(cmd, "product", "getvar", "product")
    input("\n\033[1;31mNotice\033[0m: Unlocking the bootloader will wipe all data\n\nPress Enter to unlock bootloader\n")
    os.system(f"{cmd} stage encryptData")
    os.system(f"{cmd} oem unlock")
elif "code" in r and r["code"] == 10000:
    remove("product", "token")
    sys.exit()
elif "code" in r and r["code"] == 10013:
    print(f"\n{r['descEN']}\n\nhttps://github.com/offici5l/MiUnlockTool/issues/12")
elif "code" in r and r["code"] == 20036:
    print(f"\n\033[92m{r['descEN']}\033[0m")
elif "code" in r and r["code"] in {20041, 20031, 20033, 20030, 20035}:
    print(f"\ncode {r['code']}\n\n{r['descEN']}")
else:
    for key, value in r.items():
        print(f"\n{key}: {value}")

print(p_)
print(notice)
browserp == "wlm" and input("\nPress Enter to exit ...")
