from pymafia.types import Item, Location
from pymafia.utils import get_property
from pymafia.utils import have as _have

from pymafia import ash

item = Item("protonic accelerator pack")


def have():
    """Return true if the player has the protonic accelerator pack available."""
    return _have(item)


def ghost_location():
    """Return the current location of the protonic ghost."""
    return get_property("ghostLocation", Location)


def streams_crossed():
    """Return true if the player has crossed streams today."""
    return get_property("_streamsCrossed", bool)


def cross_streams():
    """Cross streams with the target in preference "streamCrossDefaultTarget"."""
    if not have():
        raise RuntimeError("need a protonic accelerator pack")
    if streams_crossed():
        raise RuntimeError("already crossed streams today")

    ash.cli_execute("crossstreams")
