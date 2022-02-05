from enum import IntEnum
from collections import namedtuple
from pymafia import ash
from pymafia.utils import get_property


class Test(namedtuple("Test", ["id", "name", "expression"]), IntEnum):
    # fmt: off
    HP = (1, "Donate Blood", "HP")
    MUSCLE = (2, "Feed The Children", "Muscle")
    MYSTICALITY = (3, "Build Playground Mazes", "Mysticality")
    MOXIE = (4, "Feed Conspirators", "Moxie")
    FAMILIAR_WEIGHT = (5, "Breed More Collies", "Familiar Weight")
    WEAPON_DAMAGE = (6, "Reduce Gazelle Population", "Weapon Damage, Weapon Damage Percent")
    SPELL_DAMAGE = (7, "Make Sausage", "Spell Damage, Spell Damage Percent")
    NONCOMBAT = (8, "Be a Living Statue", "-combat")
    BOOZE_DROP = (9, "Make Margaritas", "Item Drop, 2 Booze Drop, -equip broken champagne bottle")
    HOT_RES = (10, "Clean Steam Tunnels", "Hot Resistance")
    COIL_WIRE = (11, "Coil Wire", "")
    DONATE = (30, "Donate Your Body To Science", "")
    # fmt: on

    def __new__(cls, *args):
        obj = super().__new__(cls, *args)
        obj._value_ = obj.id
        return obj

    def is_done(self):
        """Check if mafia currently believes this test is complete."""
        return get_property("kingLiberated", bool) or self.name in get_property("csServicesPerformed").split(",")

    def do(self):
        """Attempt to turn in the test to the Council of Loathing."""
        ash.visit_url("council.php")
        ash.run_choice(self.id)
        return self.is_done()
