from pymafia import ash, Effect, get_property, Item, Location, Macro, set_property

equipment_choices = {
    Item("LOV Eardigan"): 1,
    Item("LOV Epaulettes"): 2,
    Item("LOV Earring"): 3,
}
effect_choices = {
    Effect("Lovebotamy"): 1,
    Effect("Open Heart Surgery"): 2,
    Effect("Wandering Eye Surgery"): 3,
}
item_choices = {
    Item("LOV Enamorang"): 1,
    Item("LOV Emotionizer"): 2,
    Item("LOV Extraterrestrial Chocolate"): 3,
    Item("LOV Echinacea Bouquet"): 4,
    Item("LOV Elephant"): 5,
    Item("toast"): 6,
    None: 7,
}


def have():
    """Return true if the player has The Tunnel of L.O.V.E available."""
    return get_property("loveTunnelAvailable", bool)


def is_used():
    """Return true if The Tunnel of L.O.V.E has been used today."""
    return get_property("_loveTunnelUsed", bool)


def fight_all(equipment, effect, item, macro=Macro()):
    """Fight all LOV monsters and get buffs/equipment."""
    if not have():
        raise RuntimeError("need access to The Tunnel of L.O.V.E")
    if is_used():
        raise RuntimeError("love tunnel has already been used today")

    set_property("choiceAdventure1222", 1)  # Entrance
    set_property("choiceAdventure1223", 1)  # Fight LOV Enforcer
    set_property("choiceAdventure1224", equipment_choices[equipment])
    set_property("choiceAdventure1225", 1)  # Fight LOV Engineer
    set_property("choiceAdventure1226", effect_choices[effect])
    set_property("choiceAdventure1227", 1)  # Fight LOV Equivocator
    set_property("choiceAdventure1228", item_choices[item])
    success = ash.adv1(Location("The Tunnel of L.O.V.E."), -1, macro)

    if not success:
        raise RuntimeError("failed to use love tunnel")
