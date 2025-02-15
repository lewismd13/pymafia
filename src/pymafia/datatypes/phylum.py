from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pymafia.kolmafia import km


@dataclass(frozen=True, order=True)
class Phylum:
    phylum: Any = field(default=km.DataTypes.PHYLUM_INIT.content, compare=False)
    name: str = km.DataTypes.PHYLUM_INIT.contentString

    def __init__(self, key: str | None = None):
        if (
            isinstance(key, str) and key.casefold() == self.name.casefold()
        ) or key is None:
            return

        phylum = km.MonsterDatabase.Phylum.find(key)
        if phylum == km.MonsterDatabase.Phylum.NONE:
            raise ValueError(f"{type(self).__name__} {key!r} not found")

        object.__setattr__(self, "phylum", phylum)
        object.__setattr__(self, "name", phylum.toString())

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self)!r})"

    def __bool__(self) -> bool:
        return self != type(self)()

    @classmethod
    def all(cls) -> list[Phylum]:
        from pymafia.ash import from_java

        values = km.DataTypes.PHYLUM_TYPE.allValues()
        return sorted(from_java(values))

    @property
    def image(self) -> str:
        if self.phylum == km.MonsterDatabase.Phylum.NONE:
            return ""
        return self.phylum.getImage()
