from pymafia import ash, get_property, Item, Macro, Monster

item = Item("Witchess Set")

pieces = [
    Monster("Witchess Pawn"),
    Monster("Witchess Knight"),
    Monster("Witchess Bishop"),
    Monster("Witchess Rook"),
    Monster("Witchess Ox"),
    Monster("Witchess King"),
    Monster("Witchess Witch"),
    Monster("Witchess Queen"),
]

def have():
    """Return true if the player has the Witchess Set in their campground."""
    return item in ash.get_campground()


def fights_today():
    return get_property("_witchessFights", int)


def fights_left():
    return 5 - fights_today()


def buff_used():
    return get_property("_witchessBuff", bool)


def fight(piece, macro=Macro()):
    if not have():
        raise RuntimeError("need a Witchess Set installed")
    if fights_left() < 1:
        raise RuntimeError("out of Witchess fights")
    if piece not in pieces:
        raise ValueError(f"unknown piece: {piece!r}")
    
    ash.visit_url("campground.php?action=witchess")
    ash.run_choice(1)
    ash.visit_url(
        f"choice.php?option=1&pwd={ash.my_hash()}&whichchoice=1182&piece={piece.id}",
        False,
    )
    ash.run_combat(macro)
