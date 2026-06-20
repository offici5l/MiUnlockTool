# What is `encryptData`?

It is the `deviceToken` signed by Xiaomi's server.

---

## What is `deviceToken`?

`deviceToken` is a value retrieved via:

```
fastboot getvar token
```
or on MediaTek devices:
```
fastboot oem get_token
```

It contains device-specific information.

For example, on all modern devices the token includes the following fields:

- `1` is the value of `version` (fixed)
- `1` or `2` is the value of `tokenversion` (fixed)
- Random data e.g. `ebdbf1635ecc3899c74190f9` is the value of `nonce` (not fixed , a new value is generated every time the device reboots, which is why the `deviceToken` changes each time, and this is what makes `encryptData` expire immediately after a reboot)
- Device codename (fixed)
- Unique processor identifier `cpuid` (fixed)

---

## How does the tool work (in short)?

The tool retrieves the `deviceToken`.

It sends the `deviceToken` along with some information to Xiaomi's server via `/api/v3/ahaUnlock`.

If the account meets all requirements , including the mandatory waiting period , Xiaomi's server signs the `deviceToken` using a private key that only they possess, and returns the signature in the response as `encryptData`:

```json
{
  "code": 0,
  "description": "私钥签名成功",
  "encryptData": "signed deviceToken",
  "uid": "Xiaomi account ID"
}
```

The tool converts the `encryptData` value into raw bytes, saves it as a file, and sends it to the device via:

```
fastboot stage <encryptData_file>
```
then:
```
fastboot oem unlock
```

The device verifies the signature using Xiaomi's public key, which is permanently embedded in the firmware. If verification succeeds, the device is permanently marked as unlocked ( meaning the bootloader gets unlocked. )

---
