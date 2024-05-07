#!/usr/bin/python

import os

for lib in ['Cryptodome', 'urllib3', 'requests', 'colorama']:
    try:
        __import__(lib)
    except ImportError:
        print(f"\nInstalling {lib}...\n")
        os.system('yes | pkg update' if "com.termux" in os.getenv("PREFIX", "") else '')
        os.system(f'pip install pycryptodomex' if lib == 'Cryptodome' else f'pip install {lib}')

import re, requests, json, hmac, random, binascii, urllib, hashlib, io, urllib.parse, time, sys, urllib.request, zipfile, webbrowser, platform, subprocess, shutil, stat, datetime
from urllib3.util.url import Url
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from urllib.parse import urlparse, parse_qs, urlencode
from colorama import init, Fore, Style

init(autoreset=True)

cg = Style.BRIGHT + Fore.GREEN
cgg = Style.DIM
cr = Fore.RED
cres = Style.RESET_ALL
cy = Style.BRIGHT + Fore.YELLOW
p_ = cg + "\n" + "_"*56 +"\n"

print(cgg + "\nFor issues or feedback:\n- GitHub: github.com/offici5l/MiUnlockTool/issues\n- Telegram: t.me/Offici5l_Group\n" + cres)

print(p_)

def dw(s):
    print("\ndownload platform-tools...\n")
    url = f"https://dl.google.com/android/repository/platform-tools-latest-{s}.zip"
    cd = os.path.join(os.path.dirname(__file__))
    fp = os.path.join(cd, os.path.basename(url))    
    urllib.request.urlretrieve(url, fp)    
    with zipfile.ZipFile(fp, 'r') as zip_ref:
        zip_ref.extractall(cd)
    os.remove(fp)

up = os.path.join(os.getenv("PREFIX", ""), "bin", "miunlock")
ttp = f"\nuse command: {cg}miunlock{cres}\n"

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
        print("\ncom.termux.api app is not installed\nPlease install it first : \n\nhttps://github.com/termux/termux-api/releases/download/v0.50.1/termux-api_v0.50.1+github-debug.apk")
        exit()
    cmd = "fastboot"
    datafile = os.path.expanduser("~/data.json")
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
        if '1' in sys.argv:
            break
        elif data and data.get("login") == "ok":
            choice = input(f"\nYou are already logged in with account uid: {data['uid']}\n{cg}Press Enter to continue\n{cgg}(to log out, type 2 and press Enter){cres}\n").strip().lower()
            if choice == "2":
                os.remove(datafile)
                break
            else:
                break
        else:
            os.remove(datafile)
            break
    except json.JSONDecodeError:
        os.remove(datafile)

def remove(*keys):
    print(f"\n{cr}invalid {keys[0] if len(keys) == 1 else ' or '.join(keys)}{cres}\n")
    with open(datafile, "r+") as file:
        data = json.load(file)
        for key in keys:
            data.pop(key, None)
        file.seek(0)
        json.dump(data, file, indent=2)
        file.truncate()
    subprocess.run(["python", __file__, "1"])

try:
    with open(datafile, "r+") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}
    with open(datafile, 'w') as file:
        json.dump(data, file)

def save(data, path):
    with open(path, "w") as file:
        json.dump(data, file, indent=2)

if "user" not in data:
    data["user"] = input("\n\n(Xiaomi Account) Id or Email or Phone: ")
    save(data, datafile)

if "pwd" not in data:
    data["pwd"] = input("\nEnter password: ")
    save(data, datafile)

if "wb_id" not in data:
    input(f"\n{Fore.CYAN}Notice:\nIf logged in with any account in your default browser,\nplease log out before pressing Enter.\n\n{cres}{Style.BRIGHT}Press Enter{cres} to open confirmation page, \n copy link after seeing {Fore.CYAN}{Style.BRIGHT}\"R\":\"\",\"S\":\"OK\"{Style.RESET_ALL}, \n  and return here\n\n")
    conl = 'https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true&passive=false&hidden=false'
    if s == "Linux":
        os.system("xdg-open '" + conl + "'")
    else:
        webbrowser.open(conl)
    time.sleep(2)
    wb_id = parse_qs(urlparse(input("\nEnter Link: ")).query).get('d', [None])[0]
    if wb_id is None:
        print("\n\nInvalid link\n")
        subprocess.run(["python", __file__, "1"])
        sys.exit()
    data["wb_id"] = wb_id
    save(data, datafile)

user, pwd, wb_id = (data.get(key, "") for key in ["user", "pwd", "wb_id"])

datav = data

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
    if "passToken" not in p:
         print(f"\n{cr}Failed to get passToken !{cres}\n")
         datav.pop("wb_id")
         save(datav, datafile)
         exit()
    data = json.loads(requests.get("https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&_json=true&passive=true&hidden=true", headers=headers, cookies={'passToken': p['passToken'], 'userId': str(p['userId']), 'deviceId': parse_qs(urlparse(p['location']).query)['d'][0]}).text.replace("&&&START&&&", ""))

ssecurity, nonce, location = data["ssecurity"], data["nonce"], data["location"]

cookies = {cookie.name: cookie.value for cookie in session.get(location + "&clientSign=" + urllib.parse.quote_plus(b64encode(hashlib.sha1(f"nonce={nonce}".encode("utf-8") + b"&" + ssecurity.encode("utf-8")).digest())), headers=headers).cookies}

if 'serviceToken' not in cookies:
    print(f"\n{cr}Failed to get serviceToken.{cres}")
    remove("wb_id")
    sys.exit()

if "login" not in datav:
    datav["login"] = "ok"
    if "uid" not in datav:
        datav["uid"] = data['userId']
    save(datav, datafile)
    print(f"\n\n{cg}Login successful! Login saved.{cres}")

region = json.loads(session.get("https://account.xiaomi.com/pass/user/login/region?").text.replace("&&&START&&&", ""))['data']['region']

print(f"\nAccountInfo:\nid: {cg}{data['userId']}")
print(f"region: {cg}{region}{cres}")

region_config = json.loads(session.get("https://account.xiaomi.com/pass2/config?key=register").text.replace("&&&START&&&", ""))['regionConfig']

for key, value in region_config.items():
    if 'region.codes' in value and region in value['region.codes']:
        region = value['name'].lower()
        break

for arg in sys.argv:
    if arg.lower() in ['global', 'india', 'russia', 'china', 'europe']:
        region = arg
        break

g = "unlock.update.intl.miui.com"

if region == "china":
    url = g.replace("intl.", "")
elif region == "india":
    url = f"in-{g}"
elif region == "russia":
    url = f"ru-{g}"
elif region == "europe":
    url = f"eu-{g}"
else:
    url = g

def CheckB(cmd, var_name, *fastboot_args):
    message_printed = False
    while True:
        try:
            result = subprocess.run([cmd] + list(fastboot_args), capture_output=True, text=True, timeout=6)
            print(f"\n{cg}phone connected{cres}")
        except subprocess.TimeoutExpired:
            if not message_printed:
                print(f"\n{cr}Not connected to the phone{cres}\n\n")
                print("Turn off the phone,\nhold Volume Down and Power buttons to enter Bootloader,\nand connect the phone again")
                message_printed = True
            continue     
        lines = [line.split(f"{var_name}:")[1].strip() for line in result.stderr.split('\n') if f"{var_name}:" in line]
        if len(lines) > 1:
            cvalue = "".join(lines)
            return cvalue       
        return lines[0] if lines else None

print("\nCheck if device is connected in bootloader mode...\n")

product = CheckB(cmd, "product", "getvar", "product")
if not product:
    product = input("\nFailed to obtain the product!\nPlease enter it manually: ")

token = CheckB(cmd, "token", "getvar", "token")
if not token:
    token = CheckB(cmd, "token", "oem", "get_token")
    if not token:
        token = input("\nFailed to obtain the token!\nPlease enter it manually: ")

print(f"\nDeviceInfo:\nproduct: {cg}{product}")
print(f"token: {cg}{token}{cres}\n")

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
    CheckB(cmd, "serialno", "getvar", "serialno")
    print(f"\n{Fore.CYAN}An unlocked device is an easy target for malware which may damage your device or cause financial loss.\n\n" +
    (f"{Fore.RED}{Style.BRIGHT}user data will be cleared when the device is unlocked.{cres}\n" if product not in ["gemini", "ido", "kate", "kenzo", "land", "markw", "meri", "mido", "nikel", "omega", "prada", "rolex", "santoni", "venus", "wt88047"] else f"{Fore.GREEN}{Style.BRIGHT}Unlocking the device does not clear the user data{cres}\n\n"))
    input(f"{Style.BRIGHT}Press Enter to unlock bootloader{cres}\n")
    os.system(f"{cmd} stage encryptData")
    os.system(f"{cmd} oem unlock")
elif "descEN" in r:
    print(f"\ncode {r['code']}\n\n{r['descEN']}")
    if r["code"] == 20036:
        print("\nYou can unlock on:", (datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=r["data"]["waitHour"])).strftime("%Y-%m-%d %H:%M"))
    if r["code"] == 10000:
        print(f"\n{cr}invalid product or token")
else:
    for key, value in r.items():
        print(f"\n{key}: {value}")

print(p_)

browserp == "wlm" and input("\nPress Enter to exit ...")