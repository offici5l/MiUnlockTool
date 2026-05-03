from migate import get_passtoken, get_service, get_region, get_dataCenterZone

from miunlock.unlock import unlock_device
from miunlock.config import get_fastboot
from miunlock.config import console

def main():

    fastboot_cmd = get_fastboot()
    
    param = {"sid": 'unlockApi'}
    param["checkSafeAddress"] = True

    passToken = get_passtoken(param)
    if passToken is None:
        raise SystemExit(1)

    service = get_service(passToken, param)
    if service is None:
        raise SystemExit(1)

    region = get_region(passToken)
    if region is None:
        userId = passToken['userId']
        Zone = get_dataCenterZone(userId)
    else:
        console.print(f"\nAccount Region: {region}", style="green")
        if region == "CN":
            Zone = "China"
        elif region == "IN":            
            Zone = "India"
        elif region == "RU":  
            Zone = "Russia"
        elif region in {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IS", "IE", "IT", "LV", "LI", "LT", "LU", "MT", "NL", "NO", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "UK"}:
            Zone = "Europe"
        else:
            Zone = "Singapore"

    if Zone is None:
        Zone = get_dataCenterZone()
    else:
        console.print(f"\ndataCenterZone: {Zone}", style="green")
        user_input = console.input("\n[white](Enter to continue, [orange]m[/orange] to change dataCenterZone)[/white][white] > [/white]").strip().lower()  
        if user_input == "m":  
            Zone = get_dataCenterZone()   

    domain = {
        "Singapore": "https://unlock.update.intl.miui.com",
        "China": "https://unlock.update.miui.com",
        "India": "https://in-unlock.update.intl.miui.com",
        "Russia": "https://ru-unlock.update.intl.miui.com",
        "Europe": "https://eu-unlock.update.intl.miui.com",
    }.get(Zone)

    unlock_device(domain, service, fastboot_cmd)

if __name__ == "__main__":
    main()