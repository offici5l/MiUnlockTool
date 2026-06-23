# FAQ

## Getting an error code? 

See: [miunlock codes & messages reference](miunlock-codes-reference.md)

---

## What is encryptData?

[See](encryptData.md)

---

## How does the tool work?

[See](encryptData.md)

---

## Do I need to add my account in Developer Options?

**Yes**

Enable Developer Options (tap 7 times on MIUI version / Build number), then go to:  
**Settings → Additional settings → Developer options → Mi Unlock status**  
and tap **"Add account and device"**

---

## Do I need permission from Xiaomi Community?

**Yes** if ROM version **HyperOS**

---

## Does this tool bypass the waiting period?

**No.**

MiUnlockTool follows the **exact same official process** as Xiaomi’s official tool.  
So It is simply an **alternative tool**


---

## Will my Data Be wiped After Unlocking the Bootloader?

```miunlock``` will tell you whether your data will be wiped or not before proceeding.

> [!WARNING]
> As a general rule, **bootloader unlocking wipes all user data**. Back up your device before unlocking.

#### Exception — Legacy Devices (No Data Wipe)

The following device codenames are unlocked **without** clearing user data:

`gemini`, `ido`, `kate`, `kenzo`, `land`, `markw`, `meri`, `mido`, `nikel`, `omega`, `prada`, `rolex`, `santoni`, `venus`, `wt88047`

Device codenames of respective brands can be found below:

[Xiaomi](https://en.wikipedia.org/wiki/List_of_Xiaomi_products#Current) [Redmi](https://en.wikipedia.org/wiki/List_of_Redmi_products#Phones) [POCO](https://en.wikipedia.org/wiki/Poco_(smartphone)#Smartphones)

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
