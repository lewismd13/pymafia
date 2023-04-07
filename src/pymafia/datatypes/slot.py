from __future__ import annotations

from functools import total_ordering
from typing import Any

from pymafia.kolmafia import km

# The name property of km.Slot is inaccessible, most likely due to a collision with java's Enum.name()
NAMES = {e.value: e.key for e in km.Slot.nameToSlot.entrySet()}


@total_ordering
class Slot:
    name: str = "none"

    def __init__(self, key: str | None = None):
        if (
            isinstance(key, str) and key.casefold() == self.name.casefold()
        ) or key is None:
            return

        slot = km.EquipmentRequest.slotNumber(key)
        if slot == km.Slot.NONE:
            raise ValueError(f"{type(self).__name__} {key!r} not found")

        self.name = NAMES[slot]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self)!r})"

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.name == other.name
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.name < other.name
        return NotImplemented

    def __bool__(self) -> bool:
        return self.name != type(self).name

    @classmethod
    def all(cls) -> list[Slot]:
        from pymafia import ash

        values = km.DataTypes.SLOT_TYPE.allValues()
        return sorted(ash.to_python(values))
