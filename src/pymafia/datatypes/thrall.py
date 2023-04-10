from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pymafia.kolmafia import km

if TYPE_CHECKING:
    from .skill import Skill


@dataclass(frozen=True, order=True)
class Thrall:
    id: int = 0
    type: str = "none"

    def __init__(self, key: int | str | None = None):
        if (isinstance(key, str) and key.casefold() == self.type.casefold()) or key in (
            self.id,
            None,
        ):
            return

        data = (
            km.PastaThrallData.typeToData(key)
            if isinstance(key, str)
            else km.PastaThrallData.idToData(key)
        )
        if data is None:
            raise ValueError(f"{type(self).__name__} {key!r} not found")

        object.__setattr__(self, "id", km.PastaThrallData.dataToId(data))
        object.__setattr__(self, "type", km.PastaThrallData.dataToType(data))

    def __str__(self) -> str:
        return self.type

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self)!r})"

    def __bool__(self) -> bool:
        return (self.id, self.type) != (type(self).id, type(self).type)

    @classmethod
    def all(cls) -> list[Thrall]:
        from pymafia.conversion import from_java

        values = km.DataTypes.THRALL_TYPE.allValues()
        return sorted(from_java(values))

    @property
    def data(self) -> Any:
        return km.PastaThrallData.idToData(self.id)

    @property
    def thrall(self) -> Any:
        return km.KoLCharacter.findPastaThrall(self.type)

    @property
    def name(self) -> str:
        return self.thrall.getName() if self.thrall else ""

    @property
    def level(self) -> int:
        return self.thrall.getLevel() if self.thrall else 0

    @property
    def image(self) -> str:
        return km.PastaThrallData.dataToImage(self.data) if self else ""

    @property
    def tinyimage(self) -> str:
        return km.PastaThrallData.dataToTinyImage(self.data) if self else ""

    @property
    def skill(self) -> Skill:
        from .skill import Skill

        return Skill(km.PastaThrallData.dataToSkillId(self.data) if self else None)

    @property
    def current_modifiers(self) -> str:
        return self.thrall.getCurrentModifiers() if self.thrall else ""
