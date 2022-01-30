from pymafia import ash, get_property


def have():
    """Return true if the player has the Boxing Daycare open."""
    return get_property("daycareOpen", bool)


def daydream():
    """Have a Boxing Daydream."""
    if not have() or get_property("_daycareNap", bool):
        return False

    ash.visit_url("place.php?whichplace=town_wrong&action=townwrong_boxingdaycare")
    ash.run_choice(1)
    return True


def scavenge(turns=0):
    """Scavenge for gym equipment. The first scavenge each day is free."""
    times = turns + get_property("_daycareGymScavenges", int) == 0
    if not have() or ash.my_adventures() < turns or times <= 0:
        return False

    ash.visit_url("place.php?whichplace=town_wrong&action=townwrong_boxingdaycare")
    ash.run_choice(3)
    for _ in range(times):
        ash.run_choice(2)
    return True
