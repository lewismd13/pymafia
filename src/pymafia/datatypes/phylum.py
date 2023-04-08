from __future__ import annotations

from functools import total_ordering
from typing import Any

from pymafia.kolmafia import km


@total_ordering
class Phylum:
    name: str = "none"
    phylum: Any = km.MonsterDatabase.Phylum.NONE

    def __init__(self, key: str | None = None):
        if (
            isinstance(key, str) and key.casefold() == self.name.casefold()
        ) or key is None:
            return

        phylum = km.MonsterDatabase.Phylum.find(key)
        if phylum == km.MonsterDatabase.Phylum.NONE:
            raise ValueError(f"{type(self).__name__} {key!r} not found")

        self.name = phylum.toString()
        self.phylum = phylum

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
    def all(cls) -> list[Phylum]:
        from pymafia import ash

        values = km.DataTypes.PHYLUM_TYPE.allValues()
        return sorted(ash.to_python(values))

    @property
    def image(self) -> str:
        if self.phylum == km.MonsterDatabase.Phylum.NONE:
            return ""
        return self.phylum.getImage()
