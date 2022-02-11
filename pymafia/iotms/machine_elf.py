import pymafia.kolmafia as km
from pymafia import ash
from pymafia.types import Familiar, Location
from pymafia.utils import get_property
from pymafia.utils import have as _have

familiar = Familiar("Machine Elf")
location = Location("The Deep Machine Tunnels")


def have():
    """Return True if the player has the Machine Elf in their terrarium, False otherwise."""
    return _have(familiar)


def can_duplicate():
    """Return True if the player can DMT duplicate an item this ascension, False otherwise"""
    return get_property("lastDMTDuplication", int) < ash.my_ascensions()
