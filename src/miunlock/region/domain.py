from migate.config import (
    console
)

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

    console.print("\n[white]" + "="*50 + "[/white]")
    print("Available Regions:")
    for idx, region in enumerate(available_regions, 1):
        print(f"  {idx}. {region}")
    console.print("[white]" + "="*50 + "[/white]")

    while True:
        choice = console.input(f"\n[white]Select region number (1-{len(available_regions)}): [/white]").strip()

        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_regions):
                selected = available_regions[choice_idx]
                console.print(f"\n[green]regionConfig Selected: {selected}[/green]\n")
                return selected
            else:
                console.print(f"\n[red]Invalid choice. Please enter a number between 1 and {len(available_regions)}[/red]\n")
        except ValueError:
            console.print(f"\n[red]Invalid input. Please enter a number between 1 and {len(available_regions)}[/red]\n")