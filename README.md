<div align="center">

<a href="https://github.com/offici5l/MiUnlockTool/releases/latest">
  <img src="https://img.shields.io/badge/MiUnlockTool-%23FF6900?style=flat&logo=xiaomi&logoColor=white" alt="MiUnlockTool" width="200"/>
</a>

<br>

[![Version](https://img.shields.io/pypi/v/miunlock?label=Version&labelColor=black&color=brightgreen)](https://pypi.org/project/miunlock/)
[![Changelog](https://img.shields.io/badge/Changelog-blue?style=flat&logoColor=white)](CHANGELOG.md)
[![Error Codes](https://img.shields.io/badge/Error%20Codes-orange?style=flat&logoColor=white)](https://offici5l.github.io/MiUnlockTool/error_codes)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

---

**Developed to retrieve `encryptData(token)` for Xiaomi devices to unlock the bootloader.**

**Compatible with all platforms.**

</div>

---

## Installation
<h4>
  
An automatic installer for termux can be found [here](#quick-install-for-androidtermux)

</h4>

<h3> Step 1 </h3>
<p>Install Python</p>

<details>
<summary> Windows </summary>
<br>

You can download the installer [directly](https://www.python.org/downloads/) from Python's website or via WinGet:
```sh
winget search Python.Python
# Replace 3.14 with the latest version
winget install Python.Python.3.14
```
</details>

<details>
<summary> macOS </summary>
<br>

You can download the installer [directly](https://www.python.org/downloads/) from Python's website or via [Homebrew](https://brew.sh/):
```
brew install --cask python
```
</details>


<details>
<summary> Termux </summary>
<br>
  
```
pkg i python
```

</details>

<details>
<summary> Ubuntu/Debian </summary>
<br>
  
```
sudo apt install python3 python3-venv
```

</details>

<details>
<summary> Fedora </summary>
<br>

```
sudo dnf install python3
```
</details>

<details>
<summary> Arch Linux </summary>
<br>

```
sudo pacman -S python
```
</details>

<h3> Step 2 </h3>
<p>Create a virual environment for Python under any name you want</p>

```
python3 -m venv anyname
```
<h3> Step 3 </h3>
<p>Source the approriate variables inside the anyname/bin/ directory for your commandline shell</p>

<details>
<summary> PowerShell (Windows) </summary>
<br>
  
```
anyname/bin/activate.ps1
```
</details>

<details>
<summary> bash/zsh (Default on macOS and most Linux systems) </summary>
<br>

```
source anyname/bin/activate
```
</details>

<details>
<summary> fish </summary>
<br>

```
source anyname/bin/activate.fish
```
</details>

<details>
<summary> tcsh </summary>
<br>

```
source anyname/bin/activate.csh
```
</details>

<h3> Step 4 </h3>

<p>Install MiUnlockTool</p>

```
pip install miunlock
```

---

### Quick Install for Android(Termux):

```sh
curl -sS https://raw.githubusercontent.com/offici5l/MiUnlockTool/main/.install | bash
```

## Usage

Run the command and follow the on-screen insctructions

```sh
miunlock
```
