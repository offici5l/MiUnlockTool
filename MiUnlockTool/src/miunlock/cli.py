import migate

from miunlock.domain import get_domain
from miunlock.unlock import unlock_device
from miunlock.config import get_fastboot

from migate.config import (
    console
)


def main():

    fastboot_cmd = get_fastboot()
    
    param = {"sid": 'unlockApi'}
    param["checkSafeAddress"] = True

    passToken = migate.get_passtoken(param)

    region = migate.get_region(passToken)

    regionConfig = migate.get_regionConfig(region)

    domain = get_domain(regionConfig)

    service = migate.get_service(passToken, param)
    cookies = service["cookies"]
    ssecurity = service['servicedata']["ssecurity"]
    deviceId = service['servicedata']["deviceId"]

    unlock = unlock_device(domain, ssecurity, cookies, deviceId, fastboot_cmd)

if __name__ == "__main__":
    main()
