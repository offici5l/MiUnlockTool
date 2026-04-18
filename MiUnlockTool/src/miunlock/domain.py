from migate.config import console

_DOMAINS = {
    "Singapore": "https://unlock.update.intl.miui.com",
    "China":     "https://unlock.update.miui.com",
    "India":     "https://in-unlock.update.intl.miui.com",
    "Russia":    "https://ru-unlock.update.intl.miui.com",
    "Europe":    "https://eu-unlock.update.intl.miui.com",
}


def domain(regionConfig=None):
    if regionConfig is None:
        return list(_DOMAINS.keys())
    return _DOMAINS.get(regionConfig)


def config_manually():
    regions = domain()

    console.print("[white]" + "─" * 40 + "[/white]")
    for i, region in enumerate(regions, 1):
        console.print(f"  [orange]{i}.[/orange] [white]{region}[/white]")
    console.print("[white]" + "─" * 40 + "[/white]\n")

    while True:
        choice = console.input(
            f"[white]Select (1-{len(regions)}): [/white]"
        ).strip()

        if not choice.isdigit():
            console.print("[red]Invalid input. Enter a number.[/red]\n")
            continue

        idx = int(choice) - 1
        if 0 <= idx < len(regions):
            selected = regions[idx]
            console.print(f"\n[green]✓ regionConfig selected: {selected}[/green]\n")
            return selected

        console.print(f"[red]Out of range. Enter 1–{len(regions)}.[/red]\n")


def get_domain(regionConfig):
    _domain = domain(regionConfig)

    user_input = console.input("\n[white](Enter to continue, [orange]m[/orange] to change regionConfig)[/white][white] > [/white]").strip().lower()

    if user_input == "m":
        manual_region = config_manually()
        _domain = domain(manual_region)

    return _domain