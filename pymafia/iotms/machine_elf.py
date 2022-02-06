from pymafia.kolmafia import km
from pymafia.types import Familiar, Location
from pymafia.utils import get_property
from pymafia.utils import have as _have

from pymafia import ash

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


def can_duplicate():
    return get_property("lastDMTDuplication", int) < ash.my_ascensions()
