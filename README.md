<div align="center">

# Unlock Bootloader For Xiaomi

un-lock developed to retrieve encryptData(token) for Xiaomi devices to unlock bootloader.

It is compatible with all platforms.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)

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

</details>

[![Telegram Channel](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=blue)](https://t.me/Offici5l_Channel)

# Installation:

### For Mac, Windows, Linux:

1. Install Python3.
2. Download [un-lock](https://codeload.github.com/offici5l/un-lock/zip/refs/heads/main) and run it.

### For Android:

1. Install Termux for [ARM64](https://github.com/termux/termux-app/releases/download/v0.118.0/termux-app_v0.118.0%2Bgithub-debug_arm64-v8a.apk), [armeabi](https://github.com/termux/termux-app/releases/download/v0.118.0/termux-app_v0.118.0%2Bgithub-debug_armeabi-v7a.apk), or [Universal](https://github.com/termux/termux-app/releases/download/v0.118.0/termux-app_v0.118.0%2Bgithub-debug_universal.apk).
2. Install [Termux API](https://github.com/termux/termux-api/releases/download/v0.50.1/termux-api_v0.50.1+github-debug.apk).
3. From Termux command line:
```bash
termux-setup-storage
```
```bash
yes | pkg install python3
```
```bash
curl -o $PREFIX/bin/unlock https://raw.githubusercontent.com/offici5l/un-lock/master/un-lock.py && chmod +x $PREFIX/bin/unlock
```
```bash
unlock
```