<div align="center">

### A reference for codes | messages returned by the Mi Unlock Tools

*(this reference is updated regularly)*

</div>

---

---

### Request parameter error

**Code:** 10000

**Cause:** Invalid device token or product.

**Solution:** Restart the tool. Make sure you're using the latest version.

---
---

### This device is not activated, please activate it and try to unlock it again

**Code:** 10013

**Cause:** Motherboard replacement, changed IMEI, installment purchase, or custom DNS in use.

**Solution:** Follow the steps:
- Disable custom DNS
- Switch the SIM card to the other slot
- disable and re-enable "Find my device"
- Go to **Xiaomi Account → Xiaomi Cloud → Enable Call History and Messages** using mobile data (not Wi-Fi), then go to **Settings → Xiaomi Account → Devices → Current Device** — the SIM should appear activated
- rebind the account in Developer Options

If you encounter the same problem, please wait around 24 hours and try again. If the problem persists, please contact Xiaomi.

---
---

### This device has been activated for less than 7 days, please activate it for 7 days before trying to unlock it again

**Code:** 10013

**Cause:** Likely due to the SIM card not being activated.

**Solution:** Follow the steps:
- Disable custom DNS
- Switch the SIM card to the other slot
- disable and re-enable "Find my device"
- Go to **Xiaomi Account → Xiaomi Cloud → Enable Call History and Messages** using mobile data (not Wi-Fi), then go to **Settings → Xiaomi Account → Devices → Current Device** — the SIM should appear activated
- rebind the account in Developer Options

Wait for the displayed time to expire(7days (utc +8)), then run the tool again.

---
---

### Your device's activation time is too short, please try again in \*\* hours

**Code:** 10013

**Cause:** Phone purchase or activation period hasn't exceeded 7 days yet.

**Solution:** Wait for the displayed time to expire, then run the tool again.

---
---

### Sorry, couldn't unlock more devices

**Code:** 10023

**Cause:** You're trying to unlock another device with the same account. Since 2025, only one device per year can be unlocked per account.

**Solution:** Use a new account, or wait a year.

---
---

### Sorry, couldn't unlock more devices by this account this month

**Code:** 20030

**Cause:** You already retrieved a new `encryptData` (token) this month.

**Solution:** Wait until the 1st of next month.

---
---

### Please add your account in Settings > Developer options > Mi Unlock status

**Code:** 20031

**Cause:** Account not bound in "Mi Unlock Status".

**Solution:** Go to **Developer Options → Mi Unlock Status → Agree → Add account and device**.

> If you've already linked the account and still get this error, manually select the `dataCenterZone` in the tool.

---
---

### Your account is not authorized to unlock. Please change to another account

**Code:** 20033

**Cause:** The account has been restricted by Xiaomi's servers due to detected suspicious activity.

**Solution:** Try enabling "Find Device" in settings. If it doesn't help, create a new account.

---
---

### Please upgrade your unlock tool

**Code:** 20035

**Cause:** The tool is using an outdated `clientVersion`.

**Solution:** If using the official tool, download the latest version. If using MiUnlockTool, update `clientVersion` to a higher value.

---
---

### Please unlock \*\*\* hours later

**Code:** 20036

> Do not add your account in MIUI again, otherwise you will wait from scratch.

**Cause:** Normal waiting period. Duration varies by device type.

**Solution:** Wait until the period is over, then restart the tool.

> If the waiting time doesn't decrease or resets to 144 hours, your account has been suspended — use a different Xiaomi account.

---
---

### 该手机已被账号 \*\*\*\* 通过查找手机锁定，无法解锁

**Code:** 20038

**Cause:** The device is locked by account \*\*\*\*.

**Solution:** Log in to account \*\*\*\* at [i.mi.com/mobile/find](https://i.mi.com/mobile/find), select the device, then disable Locate Device.

---
---

### Device basic data verification failed. This device couldn't be unlocked

**Code:** 20039

**Cause:** The device token is incomplete — it doesn't contain the full set of required data.

**Solution:** No confirmed solution at this time.

---
---

### Sorry, your Mi ID is not associated with a phone number

**Code:** 20041

**Cause:** The Xiaomi account has no linked phone number.

**Solution:** Add a phone number to your account. If the option isn't available in-app, use this link:
[account.xiaomi.com/pass/serviceLogin?checkSafePhone=true](https://account.xiaomi.com/pass/serviceLogin?checkSafePhone=true)

---
---

### Please use the common user tool on the official website

**Code:** 20045

**Cause:** Invalid server region.

**Solution:** Change `dataCenterZone` in the tool.

---
---

### The place where the account is registered does not match the place where the phone is sold

**Code:** 20045

**Cause:** Mismatch between account region and device region — e.g. using a global Xiaomi account to unlock a Chinese device, or vice versa.

**Solution:** Use a Xiaomi account from the same region as the device. Chinese device → Chinese account.

---
---

### Couldn't unlock. Please go to Mi Community to apply for authorization and try again

**Code:** 30002

**Cause:** Account not bound in "Mi Unlock Status".

**Solution:** Go to **Developer Options → Mi Unlock Status → Agree → Add account and device**.

> If you've already linked the account and still get this error, manually select the `dataCenterZone` in the tool.
