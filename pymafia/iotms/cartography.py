import re
from pymafia import ash, get_property, have as _have, Macro, Skill

passive = Skill("Comprehensive Cartography")
skill = Skill("Map the Monsters")


def have():
    """Return true if the player has the Comprehensive Cartography skill."""
    return _have(passive)


def monsters_mapped():
    """Return the number monsters that have been mapped today."""
    return get_property("_monstersMapped", int)


def map_monster(location, monster, macro=Macro()):
    """Map to a monster in a location."""
    if not have() or monsters_mapped() >= 3:
        return False

    if not get_property("mappingMonsters"):
        ash.use_skill(skill)
    ash.visit_url(location.url)
    assert (
        ash.handling_choice() and ash.last_choice() == 1435
    ), "failed to encounter the Map the Monsters noncombat adventure"

    page = ash.visit_url(
        f"choice.php?pwd=&whichchoice=1435&option=1&heyscriptswhatsupwinkwink={monster.id}"
    )
    m = re.search("<!-- MONSTERID: (\\d+) -->", page)
    assert (
        m and int(m.group(1)) == monster.id
    ), f"failed to enter combat with monster: {monster!r}"

    ash.run_combat(macro)
    return True
