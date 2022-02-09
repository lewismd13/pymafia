from pymafia.kolmafia import km

from pymafia import ash, types


class Familiar:
    id = -1
    name = "none"

    def __init__(self, key=None):
        if key in (None, self.id, self.name):
            return

        id_ = km.FamiliarDatabase.getFamiliarId(key) if isinstance(key, str) else key
        name = km.FamiliarDatabase.getFamiliarName(id_)

        if name is None:
            raise NameError(f"{type(self).__name__} {key!r} not found")

        self.id = id_
        self.name = name

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
        return self != type(self)()

    @classmethod
    def all(cls):
        values = km.DataTypes.FAMILIAR_TYPE.allValues()
        return sorted(ash.to_python(values), key=lambda x: x.id)

    @property
    def familiar(self):
        return km.KoLCharacter.findFamiliar(self.id)

    @property
    def poke_data(self):
        return km.FamiliarDatabase.getPokeDataById(self.id)

    @property
    def hatchling(self):
        return (
            types.Item(km.FamiliarDatabase.getFamiliarLarva(self.id)) if self else None
        )

    @property
    def image(self):
        return km.FamiliarDatabase.getFamiliarImageLocation(self.id)

    @property
    def nickname(self):
        return None if self.familiar is None else self.familiar.getName()

    @property
    def experience(self):
        return 0 if self.familiar is None else self.familiar.getTotalExperience()

    @property
    def charges(self):
        return 0 if self.familiar is None else self.familiar.getCharges()

    @property
    def drop_name(self):
        return km.FamiliarData.dropName(self.id)

    @property
    def drop_item(self):
        item = km.FamiliarData.dropItem(self.id)
        return None if item is None else types.Item(item.getItemId())

    @property
    def drops_today(self):
        return km.FamiliarData.dropsToday(self.id)

    @property
    def drops_limit(self):
        return km.FamiliarData.dropsToday(self.id)

    @property
    def fights_today(self):
        return km.FamiliarData.fightsToday(self.id)

    @property
    def fights_limit(self):
        return km.FamiliarData.fightDailyCap(self.id)

    @property
    def combat(self):
        return km.FamiliarDatabase.isCombatType(self.id)

    @property
    def physical_damage(self):
        return km.FamiliarDatabase.isCombat0Type(self.id)

    @property
    def elemental_damage(self):
        return km.FamiliarDatabase.isCombat1Type(self.id)

    @property
    def block(self):
        return km.FamiliarDatabase.isBlockType(self.id)

    @property
    def delevel(self):
        return km.FamiliarDatabase.isDelevelType(self.id)

    @property
    def hp_during_combat(self):
        return km.FamiliarDatabase.isHp0Type(self.id)

    @property
    def mp_during_combat(self):
        return km.FamiliarDatabase.isMp0Type(self.id)

    @property
    def other_action_during_combat(self):
        return km.FamiliarDatabase.isOther0Type(self.id)

    @property
    def hp_after_combat(self):
        return km.FamiliarDatabase.isHp1Type(self.id)

    @property
    def mp_after_combat(self):
        return km.FamiliarDatabase.isMp1Type(self.id)

    @property
    def other_action_after_combat(self):
        return km.FamiliarDatabase.isOther1Type(self.id)

    @property
    def passive(self):
        return km.FamiliarDatabase.isPassiveType(self.id)

    @property
    def underwater(self):
        return km.FamiliarDatabase.isUnderwaterType(self.id)

    @property
    def variable(self):
        return km.FamiliarDatabase.isVariableType(self.id)

    @property
    def attributes(self):
        attrs = km.FamiliarDatabase.getFamiliarAttributes(self.id)
        return [] if attrs is None else list(attrs)

    @property
    def poke_level(self):
        return 0 if self.familiar is None else self.familiar.getPokeLevel()

    @property
    def poke_level_2_power(self):
        return 0 if self.poke_data is None else self.poke_data.getPower2()

    @property
    def poke_level_2_hp(self):
        return 0 if self.poke_data is None else self.poke_data.getHP2()

    @property
    def poke_level_3_power(self):
        return 0 if self.poke_data is None else self.poke_data.getPower3()

    @property
    def poke_level_3_hp(self):
        return 0 if self.poke_data is None else self.poke_data.getHP3()

    @property
    def poke_level_4_power(self):
        return 0 if self.poke_data is None else self.poke_data.getPower4()

    @property
    def poke_level_4_hp(self):
        return 0 if self.poke_data is None else self.poke_data.getHP4()

    @property
    def poke_move_1(self):
        return None if self.poke_data is None else self.poke_data.getMove1()

    @property
    def poke_move_2(self):
        return None if self.poke_data is None else self.poke_data.getMove2()

    @property
    def poke_move_3(self):
        return None if self.poke_data is None else self.poke_data.getMove3()

    @property
    def poke_attribute(self):
        return None if self.poke_data is None else self.poke_data.getAttribute()
