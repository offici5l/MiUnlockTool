<div align="center">

# MiUnlockTool
developed to retrieve encryptData(token) for Xiaomi devices to unlock bootloader,
It is compatible with all platforms.

</div>

![Version](https://img.shields.io/badge/version-1.5.0-blue)

<details>
  <summary>show Version History</summary>

### Version 1.4.8:

- Make the installation method easier, just download and run the file, it will take care of the rest.
- Other improvements

### Version 1.4.9:

- Improvements and fixes

### Version 1.5.0:

- un-lock has been restructured and rebuilt.
- Improved and reduced un-lock size.
- un-lock is now compatible with all operating systems.
- Resolved the "securityStatus16" issue and fixed other problems.

#### Version 1.5.0 (Update):
- Deleted `cmd getvar all` in `def CheckB` and replaced it with `getvar token` and `getvar product`.
- In case of failure to obtain `deviceToken` and `product`, added a step to enter them manually.
- Other improvements

#### Version 1.5.0 (Update):
- Simplified cookie extraction for concise code.
- Streamlined URL determination for better clarity based on the geographical region.
- Specified "https" directly in the `Url` constructor for secure communication and improved clarity.
- Deleted requests to "/api/v3/unlock/userinfo" and "/api/v2/unlock/device/clear" to reduce code size as they are not currently important.
- Adjusted message formatting for enhanced readability.
- Changed `cmd = "tfastboot"` to `cmd = "fastboot"`. Also, removed `adb`.

### Tool name update: "un-lock" is now "MiUnlockTool".

#### Version 1.5.0 (Update):
- Minor bug fix
- Add command (cmd, "oem", "get_token")
- In the event of failure to obtain the device token, the user will be asked to enter it manually
- Other improvements

#### Version 1.5.0 (Update):
- When 2 or more tokens are obtained via the festboot oem get_token ..
tool will now merge them automatically

</details>

[![Telegram Channel](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=blue)](https://t.me/Offici5l_Channel)

# Installation:

### For Mac, Windows, Linux:

1. Install Python3.
2. Download [MiUnlockTool](https://codeload.github.com/offici5l/MiUnlockTool/zip/refs/heads/main) and run it.

### For Android:

1. Install [Termux](https://github.com/termux/termux-app/releases/tag/v0.118.0)

2. Install [Termux API](https://github.com/termux/termux-api/releases/download/v0.50.1/termux-api_v0.50.1+github-debug.apk)

3. From Termux command line:
```bash
termux-setup-storage
```
```bash
yes | pkg install python3
```
```bash
curl -O https://raw.githubusercontent.com/offici5l/MiUnlockTool/master/MiUnlockTool.py && python MiUnlockTool.py
```

<div align="center">

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)

</div>
