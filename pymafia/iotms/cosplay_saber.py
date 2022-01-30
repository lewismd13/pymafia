from pymafia import ash, get_property, have as _have, Item

item = Item("Fourth of May Cosplay Saber")
upgrades = ["mp", "ml", "resistance", "familiar"]


def have():
    """Return true if the player has the Fourth of May Cosplay Saber available."""
    return _have(item)


def is_upgraded():
    """Return true if the Fourth of May Cosplay Saber has been upgraded."""
    return get_property("_saberMod", int) != 0


def upgrade(new_upgrade):
    """Upgrade the Fourth of May Cosplay Saber."""
    if new_upgrade not in upgrades:
        raise ValueError(f"unexpected value for new_upgrade: {new_upgrade!r}")
    if not have() or is_upgraded():
        return False

    ash.cli_execute(f"saber {new_upgrade}")
    return True
