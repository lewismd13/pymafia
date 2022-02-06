from pymafia.types import Item
from pymafia.utils import get_property
from pymafia.utils import have as _have

from pymafia import ash

item = Item("Kramco Sausage-o-Matic™")


def have():
    """Return true if the player has the Kramco Sausage-o-Matic™ available."""
    return _have(item)


def is_fight_ready():
    """Return true if the maximum turns between sausage goblins has been reached."""
    if not have():
        return False

    total_fought = get_property("_sausageFights", int)
    last_turn = get_property("_lastSausageMonsterTurn", int)
    ready_on = last_turn + 4 + 3 * total_fought + max(0, total_fought - 5) ** 3
    return ash.total_turns_played() >= ready_on
