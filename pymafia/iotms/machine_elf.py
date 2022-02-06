from pymafia import Familiar, have as _have, km, Location

familiar = Familiar("Machine Elf")
location = Location("The Deep Machine Tunnels")


def have():
    """Return true if the player has the Machine Elf in their terrarium."""
    return _have(familiar)


def fights_today():
    """Free Deep Machine Tunnel fights used today."""
    return km.FamiliarData.fightsToday(familiar.id)


def fights_left():
    """Free Deep Machine Tunnel fights left today."""
    return 5 - fights_today()
