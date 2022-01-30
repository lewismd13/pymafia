from pymafia import ash, Familiar, get_property, have as _have, Item, Macro

familiar = Familiar("God Lobster")

reward_choices = {"regalia": 1, "blessing": 2, "experience": 3}
regalia = [
    Item("God Lobster's Scepter"),
    Item("God Lobster's Ring"),
    Item("God Lobster's Rod"),
    Item("God Lobster's Robe"),
    Item("God Lobster's Crown"),
]


def have():
    """Return true if the player has the God Lobster in their terrarium."""
    return _have(familiar)


def fights_today():
    """Return the number of God Lobster fights used today."""
    return get_property("godLobsterFights", int)


def fights_left():
    """Return the number of God Lobster fights remaining today."""
    return 3 - fights_today()


def fight(reward, macro=Macro()):
    """Fight the God Lobster and choose a reward."""
    if not have() or fights_left() < 1:
        return False

    choice = reward_choices[reward]
    ash.use_familiar(familiar)
    if reward == "regalia":
        for item in regalia[::-1]:
            if _have(item):
                ash.equip(item)
                break
    ash.visit_url("main.php?fightgodlobster=1")
    ash.run_combat(macro)
    ash.run_choice(choice)
    return True
