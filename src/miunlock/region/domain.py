from colorama import Fore, Style

def domain(regionConfig=None):

    domains = {
        "Singapore": "https://unlock.update.intl.miui.com",
        "China": "https://unlock.update.miui.com",
        "India": "https://in-unlock.update.intl.miui.com",
        "Russia": "https://ru-unlock.update.intl.miui.com",
        "Europe": "https://eu-unlock.update.intl.miui.com",
    }
    
    if regionConfig is None:
        return list(domains.keys())

    return domains.get(regionConfig)


def config_manually():
    available_regions = domain()

    print("\n" + Fore.CYAN + "="*50)
    print("Available Regions:")
    for idx, region in enumerate(available_regions, 1):
        print(f"  {idx}. {region}")
    print("="*50 + Style.RESET_ALL)

    while True:
        choice = input(f"\n{Fore.CYAN}Select region number (1-{len(available_regions)}): ").strip()

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_regions):
                selected = available_regions[choice_idx]
                print(f"\n{Fore.GREEN}regionConfig Selected: {selected}\n")
                return selected
            else:
                print(f"\n{Fore.RED}Invalid choice. Please enter a number between 1 and {len(available_regions)}\n")
        except ValueError:
            print(f"\n{Fore.RED}Invalid input. Please enter a number between 1 and {len(available_regions)}\n")