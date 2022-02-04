import math
from enum import Enum
from pymafia import ash
from pymafia.types import Effect, Familiar, Item, Slot, Stat
from pymafia.utils import get_property, have
from pymafia.iotms import song_boom


class Test(Enum):
    HP = (1, "Donate Blood")
    MUSCLE = (2, "Feed The Children")
    MYSTICALITY = (3, "Build Playground Mazes")
    MOXIE = (4, "Feed Conspirators")
    FAMILIAR_WEIGHT = (5, "Breed More Collies")
    WEAPON_DAMAGE = (6, "Reduce Gazelle Population")
    SPELL_DAMAGE = (7, "Make Sausage")
    NONCOMBAT = (8, "Be a Living Statue")
    BOOZE_DROP = (9, "Make Margaritas")
    HOT_RES = (10, "Clean Steam Tunnels")
    COIL_WIRE = ((11, "Coil Wire"),)
    DONATE = (30, "Donate Your Body To Science")

    def predict(self):
        if self is self.HP:
            return 60 - math.floor(
                (ash.my_maxhp() - ash.my_buffedstat(Stat.MUSCLE) - 3) / 30
            )
        if self in [self.MUSCLE, self.MYSTICALITY, self.MOXIE]:
            stat = Stat[self.name]
            return 60 - math.floor(
                (1 / 30) * (ash.my_buffedstat(stat) - ash.my_basestat(stat))
            )
        if self is self.FAMILIAR_WEIGHT:
            return 60 - math.floor(
                (ash.familiar_weight(ash.my_familiar()) + ash.weight_adjustment()) / 5
            )
        if self is self.WEAPON_DAMAGE:
            weapon_power = ash.get_power(ash.equipped_item(Slot.WEAPON))
            offhand_power = (
                ash.get_power(ash.equipped_item(Slot.OFFHAND))
                if ash.to_slot(ash.equipped_item(Slot.OFFHAND)) == Slot.WEAPON
                else 0
            )
            familiar_power = (
                ash.getPower(ash.equipped_item(Slot.FAMILIAR))
                if ash.toSlot(ash.equipped_item(Slot.FAMILIAR)) == Slot.WEAPON
                else 0
            )
            song_damage = (
                ash.my_level()
                if song_boom.song() == "These Fists Were Made for Punchin'"
                else 0
            )

            # mafia does not currently count swagger
            multiplier = 2 if have(Effect("Bow-Legged Swagger")) else 1
            return (
                60
                - math.floor(
                    (
                        multiplier
                        * (
                            ash.numeric_modifier("Weapon Damage")
                            - 0.15 * (weapon_power + offhand_power + familiar_power)
                            - song_damage
                        )
                    )
                    / 50
                    + 0.001
                )
                - math.floor(
                    (multiplier * ash.numeric_modifier("Weapon Damage Percent")) / 50
                    + 0.001
                )
            )
        if self is self.SPELL_DAMAGE:
            dragonfish_damage = (
                ash.numeric_modifier(
                    Familiar("Magic Dragonfish"),
                    "Spell Damage Percent",
                    ash.familiar_weight(Familiar("Magic Dragonfish"))
                    + ash.weight_adjustment(),
                    Item(None),
                )
                if ash.my_familiar() == Familiar("Magic Dragonfish")
                else 0
            )
            return (
                60
                - math.floor(ash.numeric_modifier("Spell Damage") / 50 + 0.001)
                - math.floor(
                    (ash.numeric_modifier("Spell Damage Percent") - dragonfish_damage)
                    / 50
                    + 0.001
                )
            )
        if self is self.NONCOMBAT:
            noncombat_rate = -1 * ash.numeric_modifier("Combat Rate")
            unsoftcapped_rate = (
                25 + (noncombat_rate - 25) * 5
                if noncombat_rate > 25
                else noncombat_rate
            )
            return 60 - 3 * math.floor(unsoftcapped_rate / 5)
        if self is self.BOOZE_DROP:
            familiar_item_drop = ash.numeric_modifier(
                ash.my_familiar(),
                "Item Drop",
                ash.familiar_weight(ash.my_familiar()) + ash.weight_adjustment(),
                ash.equipped_item(Slot.FAMILIAR),
            )

            # Champagne doubling does NOT count for CS, so we undouble
            multiplier = (
                0.5
                if ash.have_equipped(Item("broken champagne bottle"))
                and get_property("garbageChampagneCharge", int) > 0
                else 1
            )

            return (
                60
                - multiplier
                * math.floor(
                    (ash.numeric_modifier("Item Drop") - familiar_item_drop) / 30
                    + 0.001
                )
                - math.floor(ash.numeric_modifier("Booze Drop") / 15 + 0.001)
            )
        if self is self.HOT_RES:
            return 60 - ash.numeric_modifier("Hot Resistance")
        if self is self.COIL_WIRE:
            return 60
        if self is self.DONATE:
            return 0

    def maximize(self):
        pass

    def is_done(self):
        pass

    def do(self):
        pass
