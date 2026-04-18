# FAQ

## Getting an error code? 

See: [answer error codes](https://offici5l.github.io/MiUnlockTool/error_codes)

---

## Will my Data Be wiped After Unlocking the Bootloader?

```miunlock``` will tell you whether your data will be wiped or not before proceeding.

> [!WARNING]
> As a general rule, **bootloader unlocking wipes all user data**. Back up your device before unlocking.

#### Exception — Legacy Devices (No Data Wipe)

The following device codenames are unlocked **without** clearing user data:

`gemini`, `ido`, `kate`, `kenzo`, `land`, `markw`, `meri`, `mido`, `nikel`, `omega`, `prada`, `rolex`, `santoni`, `venus`, `wt88047`

---

## Does this tool bypass the waiting period?

No. MiUnlockTool follows the same official flow as Xiaomi's own tool.

---

## Why is my device not being detected?

- If On Android (Termux): make sure your phone supports OTG and that it is enabled
- If On Windows: the device should appear in Device Manager without a warning icon — install Xiaomi USB drivers — [xiaomi_usb_driver](http://bigota.d.miui.com/tools/xiaomi_usb_driver.rar)
- Make sure the device is in fastboot mode
- Try a different USB data cable — prefer the original
- Unplug and replug the cable and make sure it's connected properly
- remove any previously installed ADB/Fastboot and let the miunlock use its own


---

If you can't find an answer, check [closed issues](https://github.com/offici5l/MiUnlockTool/issues?q=is%3Aissue+is%3Aclosed) or [open a new one](https://github.com/offici5l/MiUnlockTool/issues/new).