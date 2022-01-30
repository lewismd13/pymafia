from pymafia import ash, get_property, have as _have, Item

item = Item("mumming trunk")

costume_choices = {
    "meat": 0,
    "mp": 1,
    "musc": 2,
    "item": 3,
    "myst": 4,
    "hp": 5,
    "mox": 6,
}


def have():
    """Return true if the player has the mumming trunk available."""
    return _have(item)


def choose_costume(costume):
    """Dress up the player's current familiar with a costume."""
    choice = costume_choices[costume]

    if (
        not have()
        or not ash.my_familiar()
        or str(choice) in get_property("_mummeryUses")
    ):
        return False

    ash.cli_execute(f"mummery {costume}")
    return True
