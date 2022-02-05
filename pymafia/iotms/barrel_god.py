import re

from pymafia.utils import get_property

from pymafia import ash


def have():
    """Return true if the player has the shrine to the Barrel god unlocked."""
    return get_property("barrelShrineUnlocked", bool)


def smash_free():
    """Smash the free barrels in The Barrel full of Barrels."""
    if not have():
        raise RuntimeError("need a shrine to the Barrel god installed")

    pattern = '<div class="ex"><a class="spot" href="([^"]+)"><img title="A barrel"'
    for barrel in re.findall(pattern, ash.visit_url("barrel.php")):
        ash.visit_url(barrel)
