from pymafia import ash, get_property, have as _have, Item, Location

item = Item("protonic accelerator pack")


def have():
    return _have(item)


def ghost_location():
    return get_property("ghostLocation", Location)


def streams_crossed():
    return get_property("_streamsCrossed", bool)


def cross_streams():
    if not have() or streams_crossed():
        return False

    ash.cli_execute("crossstreams")
    return True
