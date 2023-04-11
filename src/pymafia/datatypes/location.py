from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from jpype import JClass

from pymafia.kolmafia import km

if TYPE_CHECKING:
    from pymafia.datatypes.bounty import Bounty

Integer = JClass("java.lang.Integer")


@dataclass(frozen=True, order=True)
class Location:
    id: int = -1
    name: str = "none"

    def __init__(self, key: int | str | None = None):
        if (isinstance(key, str) and key.casefold() == self.name.casefold()) or key in (
            self.id,
            None,
        ):
            return

        kol_adventure = (
            km.AdventureDatabase.getAdventure(key)
            if isinstance(key, str)
            else km.AdventureDatabase.getAdventureByURL(
                f"adventure.php?snarfblat={key}"
            )
        )
        if kol_adventure is None:
            raise ValueError(f"{type(self).__name__} {key!r} not found")

        object.__setattr__(self, "id", kol_adventure.getSnarfblat())
        object.__setattr__(self, "name", kol_adventure.getAdventureName())

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self)!r})"

    def __bool__(self) -> bool:
        return (self.id, self.name) != (type(self).id, type(self).name)

    @classmethod
    def all(cls) -> list[Location]:
        from pymafia.ash import from_java

        values = km.DataTypes.LOCATION_TYPE.allValues()
        return sorted(from_java(values))

    @property
    def url(self) -> str:
        return f"adventure.php?snarfblat={self.id}"

    @property
    def kol_adventure(self) -> Any:
        return km.AdventureDatabase.getAdventureByURL(self.url)

    @property
    def nocombats(self) -> bool:
        return self.kol_adventure.isNonCombatsOnly() if self else False

    @property
    def combat_percent(self) -> float:
        if not self:
            return 0
        area = self.kol_adventure.getAreaSummary()
        return 0 if area is None else area.areaCombatPercent()

    @property
    def zone(self) -> str:
        return self.kol_adventure.getZone() if self else ""

    @property
    def parent(self) -> str:
        return self.kol_adventure.getParentZone() if self else ""

    @property
    def parentdesc(self) -> str:
        return self.kol_adventure.getParentZoneDescription() if self else ""

    @property
    def environment(self) -> str:
        return self.kol_adventure.getEnvironment() if self else ""

    @property
    def bounty(self) -> Bounty:
        from pymafia.datatypes.bounty import Bounty

        if not self:
            return Bounty(None)
        bounty = km.AdventureDatabase.getBounty(self.kol_adventure)
        return Bounty(None) if bounty is None else Bounty(bounty.getName())

    @property
    def combat_queue(self) -> list[str]:
        if not self:
            return []
        zone_queue = km.AdventureQueueDatabase.getZoneQueue(self.kol_adventure)
        return [] if zone_queue is None else list(zone_queue)

    @property
    def noncombat_queue(self) -> list[str]:
        if not self:
            return []
        zone_queue = km.AdventureQueueDatabase.getZoneNoncombatQueue(self.kol_adventure)
        return [] if zone_queue is None else list(zone_queue)

    @property
    def turns_spent(self) -> int:
        return (
            km.AdventureSpentDatabase.getTurns(self.kol_adventure, True) if self else 0
        )

    @property
    def kisses(self) -> int:
        return km.FightRequest.dreadKisses(self.kol_adventure) if self else 0

    @property
    def recommended_stat(self) -> int:
        return self.kol_adventure.getRecommendedStat() if self else 0

    @property
    def poison(self) -> int:
        if not self:
            return Integer.MAX_VALUE
        area = self.kol_adventure.getAreaSummary()
        return Integer.MAX_VALUE if area is None else area.poison()

    @property
    def water_level(self) -> int:
        return (
            self.kol_adventure.getWaterLevel()
            if self and km.KoLCharacter.inRaincore()
            else 0
        )

    @property
    def wanderers(self) -> bool:
        return self.kol_adventure.hasWanderers() if self else False

    @property
    def fire_level(self) -> int:
        return (
            km.WildfireCampRequest.getFireLevel(self.kol_adventure)
            if self and km.KoLCharacter.inFirecore()
            else 0
        )
