# What is `encryptData`?

`encryptData` is the signature of the `deviceToken`, returned by Xiaomi's server after successful verification.

The `deviceToken` is "stamped" by Xiaomi using a private key that only they possess. The device then unstamps this seal using a matching public key embedded in its firmware, and compares the result against the `deviceToken` data itself. If they match, the bootloader is unlocked.

## In short, what does the tool do?

1. It retrieves the `deviceToken` from the device via:
   ```
   fastboot getvar token
   ```
   or
   ```
   fastboot oem get_token
   ```

2. It sends the `deviceToken` along with some information to the `/api/v3/ahaUnlock` endpoint.

3. If the account meets the requirements (including the required waiting period), the server returns `encryptData` in the response:
   ```json
   {
     "code": 0,
     "description": "私钥签名成功",
     "encryptData": "signed deviceToken",
     "uid": "Xiaomi account ID"
   }
   ```

4. The tool converts this signature (hex string) into raw bytes and saves it to a temporary file.

5. It passes the path of this file to the device via:
   ```
   fastboot stage <encryptData_file>
   ```
   then:
   ```
   fastboot oem unlock
   ```

## What does the device do?

After receiving the signature, the device unstamps the seal using Xiaomi's public key embedded in it, and compares the result against the `deviceToken` data itself. If they match, the device is permanently marked as unlocked, meaning the bootloader gets unlocked.
