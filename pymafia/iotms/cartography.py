import re

from pymafia.combat import Macro
from pymafia.types import Skill
from pymafia.utils import get_property
from pymafia.utils import have as _have

from pymafia import ash

passive = Skill("Comprehensive Cartography")
skill = Skill("Map the Monsters")


def have():
    """Return true if the player has the Comprehensive Cartography skill."""
    return _have(passive)


def monsters_mapped():
    """Map the Monsters skill uses today."""
    return get_property("_monstersMapped", int)


def map_monster(location, monster, macro=Macro()):
    """Map to a monster in a location."""
    if not have():
        raise RuntimeError("need the Comprehensive Cartography skill")
    if monsters_mapped() >= 3:
        raise RuntimeError("already mapped three monsters today")

    if not get_property("mappingMonsters"):
        ash.use_skill(skill)
    ash.visit_url(location.url)
    if not ash.handling_choice() or ash.last_choice() != 1435:
        raise RuntimeError("failed to encounter the Map the Monsters noncombat adventure")  # fmt: skip
    page = ash.visit_url(f"choice.php?pwd=&whichchoice=1435&option=1&heyscriptswhatsupwinkwink={monster.id}")  # fmt: skip
    match = re.search("<!-- MONSTERID: (\\d+) -->", page)
    if not match or int(match.group(1)) != monster.id:
        raise RuntimeError(f"failed to enter combat with monster: {monster!r}")
    ash.run_combat(macro)
