from functools import cached_property

from pymafia.kolmafia import km
from pymafia.types import Item

from pymafia import ash


class Familiar:
    def __init__(self, key):
        if key in (None, -1, "none"):
            self.id = -1
            self.name = "none"
            return

        id_ = int(
            km.FamiliarDatabase.getFamiliarId(key) if isinstance(key, str) else key
        )
        name = km.FamiliarDatabase.getFamiliarName(id_)

        if name is None:
            raise NameError(f"{type(self).__name__} {key!r} not found")

        self.id = id_
        self.name = name

    @classmethod
    def all(cls):
        values = km.DataTypes.FAMILIAR_TYPE.allValues()
        return sorted(ash.to_python(values), key=lambda x: x.id)

    def __hash__(self):
        return hash((self.id, self.name))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{type(self).__name__}({str(self)!r})"

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.id, self.name) == (
            other.id,
            other.name,
        )

    def __bool__(self):
        return self.name != "none"

    @cached_property
    def hatchling(self):
        return Item(km.FamiliarDatabase.getFamiliarLarva(self.id))

    @property
    def nickname(self):
        return km.KoLCharacter.findFamiliar(self.name).getName()
