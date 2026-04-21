from migate import get_passtoken, get_region, get_regionConfig, get_service

from miunlock.domain import get_domain
from miunlock.unlock import unlock_device
from miunlock.config import get_fastboot

def main():

    fastboot_cmd = get_fastboot()
    
    param = {"sid": 'unlockApi'}
    param["checkSafeAddress"] = True

    passToken = get_passtoken(param)

    region = get_region(passToken)

    regionConfig = get_regionConfig(region)

    domain = get_domain(regionConfig)

    service = get_service(passToken, param)

    unlock_device(domain, service, fastboot_cmd)

if __name__ == "__main__":
    main()
