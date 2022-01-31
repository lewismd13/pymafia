from pymafia import ash, get_property, have as _have, Item

item = Item("Fourth of May Cosplay Saber")
upgrade_choices = {"mp": 1, "ml": 2, "resistance": 3, "familiar": 4}


def have():
    """Return true if the player has the Fourth of May Cosplay Saber available."""
    return _have(item)


def current_upgrade():
    """Return the current Fourth of May Cosplay Saber upgrade."""
    mod = get_property("_saberMod", int)
    for name, choice in upgrade_choices.items():
        if choice == mod:
            return name
    return None


def is_upgraded():
    """Return true if the Fourth of May Cosplay Saber has been upgraded today."""
    return current_upgrade() is not None


def upgrade(new_upgrade):
    """Upgrade the Fourth of May Cosplay Saber."""
    if not have():
        raise RuntimeError("need a Fourth of May Cosplay Saber")
    if is_upgraded() and current_upgrade() == new_upgrade:
        return
    if is_upgraded():
        raise RuntimeError("already upgraded the saber today")
    if new_upgrade not in upgrade_choices:
        raise ValueError(f"unknown upgrade: {new_upgrade!r}")

    success = ash.cli_execute(f"saber {new_upgrade}")

    if not success:
        raise RuntimeError("failed to upgrade the saber with {new_upgrade!r}")  # fmt: skip
