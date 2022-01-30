from pymafia import ash, Element, Familiar, get_property, have as _have, Item, Stat

familiar = Familiar("Crimbo Shrub")
decorations = Item("box of old Crimbo decorations")

topper_choices = {Stat.MUSCLE: 1, Stat.MYSTICALITY: 2, Stat.MOXIE: 3}
lights_choices = {
    "prismatic": 1,
    Element.HOT: 2,
    Element.COLD: 3,
    Element.STENCH: 4,
    Element.SPOOKY: 5,
    Element.SLEAZE: 6,
}
garland_choices = {"hp": 1, "pvp": 2, "blocking": 3}
gift_choices = {"yellow": 1, "meat": 2, "gifts": 3}


def have():
    """Return true if the player has the Crimbo Shrub in their terrarium."""
    return _have(familiar)


def is_decorated():
    """Return true if the Crimbo Shrub has been decorated today."""
    return get_property("_shrubDecorated", bool)


def decorate(topper, lights, garland, gift):
    """Decorate the Crimbo Shrub."""
    if not have() or is_decorated():
        return False

    choices = (
        topper_choices[topper],
        lights_choices[lights],
        garland_choices[garland],
        gift_choices[gift],
    )
    ash.visit_url(f"inv_use.php?pwd=&which=99&whichitem={decorations.id}")
    ash.visit_url(
        f"choice.php?whichchoice=999&pwd=&option=1&topper={choices[0]}&lights={choices[1]}&garland={choices[2]}&gift={choices[3]}"
    )
    return True
