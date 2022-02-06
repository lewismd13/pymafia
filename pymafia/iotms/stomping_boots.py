from pymafia.types import Familiar
from pymafia.utils import get_property
from pymafia.utils import have as _have

from pymafia import ash

familiar = Familiar("Pair of Stomping Boots")


def have():
    """Return true if the player has the Pair of Stomping Boots in their terrarium."""
    return _have(familiar)


def runaways_used():
    """Free runaways that have already been used."""
    return get_property("banderRunaways", int)


def runaways_left():
    """Remaining free runaways the player can get from their Stomping Boots."""
    return (ash.familiar_weight(familiar) + ash.weight_adjustment()) // 5
