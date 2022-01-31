from pymafia import ash, get_property, have as _have, Item, Location

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

    success = ash.cli_execute("crossstreams")

    if not success:
        raise RuntimeError("failed to cross streams")
