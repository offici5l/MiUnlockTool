<details markdown='1'><summary>code 10013 = This device  is not activated, please activate it and try to unlock it again</summary>

___

the issue is due to changing a piece of the phone's hardware, most likely the motherboard

Currently, there is no solution for this issue unfortunately

The only solution currently is to contact the Xiaomi support team.

___

### Explanation of the reason according to my analysis:

When sending a request to Xiaomi's server through developer settings "Mi Unlock status" the following information is sent to Xiaomi's server for verification:
- userId
- rom_version
- heartbeat_mode
- cloudsp_devId
- cloudsp_cpuId
- cloudsp_product
- cloudsp_userId
- cloudsp_fid
- cloudsp_nonce
- cloudp_sign
- error_code

I believe the issue is related to cloudsp_fid, which is the security DeviceId.

Therefore, Xiaomi's server, upon analyzing the security DeviceId, returns error code 10013 when attempting to unlock the bootloader.

</details>

___

<details markdown='1'><summary>code 20030 = Sorry, couldn't unlock more devices by this account this month</summary>

___

The reason is because you have already unlocked a device recently from one Mi account at once

You must wait for the beginning of next month, meaning the 1st of next month ( according to the time zone of the server region )

___

**Question:**
But I haven't unlocked any device before!

**Answer:**
Yes, but you have used a bootloader unlocking tool before (or **reason**) with the same account (whether it's official or unofficial doesn't matter).
The Xiaomi server has indeed sent the encryptedData(token) before, to unlock the bootloader. So, whether you have previously unlocked a device or failed to unlock the same device, it doesn't matter. Because new data (with the same account) For some **Reason**(explained at the end of the answer) was sent to the server that doesn't match the data sent in the initial attempt. Therefore, the Xiaomi server considers that you're attempting to unlock a new device, and it only allows unlocking one device per month.

**Reason: after the last encryptedData(token) received from the server**(
- The account has logged out on the device Then are logged in(This generates a mismatched device token)
-  An attempt was made to send the request in developer settings("add account and device")
- And other reasons

) ****Conclusion: data no longer matches > So Xiaomi's server considers it a new device****

</details>

___

<details markdown='1'><summary>code 20035 = Please upgrade your unlock tool.</summary>

___

If you are using an official tool or other tools Download the latest version of the tool.

If you are using the MiUnlockTool, Just update "clientVersion":"Place a higher version than the previous one"

You find it in the file MiUnlockTool.py., in the line containing :
r = RetrieveEncryptData("/api/v3/ahaUnlock", {"appId":"1", "data":{"clientId":"2", "clientVersion":"7.6.727.43", .........

</details>

___

<details markdown='1'><summary>code 10000 = Request parameter error</summary>

___

invalid device "token or product"

</details>

