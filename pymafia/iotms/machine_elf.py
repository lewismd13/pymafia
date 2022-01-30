from pymafia import km, have as _have, Familiar, Location

familiar = Familiar("Machine Elf")
location = Location("The Deep Machine Tunnels")


def have():
    """Return true if the player has the Machine Elf in their terrarium."""
    return _have(familiar)


def fights_today():
    """Return the number of free Deep Machine Tunnel fights used today"""
    return km.FamiliarData.fightsToday(familiar.id)


def fights_left():
    """Return the number of free Deep Machine Tunnel fights remaining today"""
    return 5 - fights_today()
