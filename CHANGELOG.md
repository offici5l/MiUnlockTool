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

#### Version 1.5.0 (Update):
- Updated client version to 7.6.727.43.
- Improved unlocking process.

#### Version 1.5.0 (Update):
- Save keys:values ​​directly

#### Version 1.5.0 (Update):
- Added a step to check if the com.termux.api application is installed ..

#### Version 1.5.0 (Update):
- A few users are experiencing an issue regarding "Check if device is connected in bootloader mode..."
Due to the slow transmission with the device
So the time was increased from 1s to [6s](https://github.com/offici5l/MiUnlockTool/blob/main/MiUnlockTool.py#L112)

#### Version 1.5.0 (Update):
- get tokens(deviceToken) and merging them Automatically done. ( MTK devices )

#### Version 1.5.0 (Update):
- Add ability to choose server(host region) from terminal

#### Version 1.5.0 (Update):
- Adding some improvements

#### Version 1.5.0 (Update):
- improvements

#### Version 1.5.0 (Update):
- Skip saving device information such as token and product, so as not to cause problems during unlocking...
- improvements

#### Version 1.5.0 (Update):
- Adding some improvements

#### Version 1.5.0 (Update):
- Correct the issue of the confirmation page not opening in Linux

#### Version 1.5.0 (Update):
- fix ( For Linux( and termux ) users : the 401 issue .... during account confirmation ... )

#### Version 1.5.0 (Update):
- add colorama to handle colors instead of ANSI
- Add requests to access the region and deal with the region, to send the request to the correct server accurately
- improvements

#### Version 1.5.0 (Update):
- Adding some improvements

#### Version 1.5.0 (Update):
- Add manual mode to unlock the bootloader

#### Version 1.5.0 (Update):
- Enhanced request security and improved access to region data to fix issues "code 20033"

#### Version 1.5.0 (Update):
- Replace command "oem device-info" with "getvar unloked"

#### Version 1.5.0 (Update):
- Adding steps to deal with "security Status 4", regarding adding email to xiaomi account This will fix "Failed to get pass Token"