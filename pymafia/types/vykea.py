from enum import IntEnum

from pymafia.kolmafia import km

from pymafia import ash, types


class VykeaType(IntEnum):
    NONE = km.VYKEACompanionData.NONE
    BOOKSHELF = km.VYKEACompanionData.BOOKSHELF
    DRESSER = km.VYKEACompanionData.DRESSER
    CEILING_FAN = km.VYKEACompanionData.CEILING_FAN
    COUCH = km.VYKEACompanionData.COUCH
    LAMP = km.VYKEACompanionData.LAMP
    DISHRACK = km.VYKEACompanionData.DISHRACK


class Vykea:
    companion = km.VYKEACompanionData.NO_COMPANION

    def __init__(self, key=None):
        if key in (None, "none"):
            return

        companion = km.VYKEACompanionData.fromString(key)

        if companion is None:
            raise NameError(f"{type(self).__name__} {key!r} not found")

        self.name = companion.getName()
        self.companion = companion

    def __hash__(self):
        return hash((self.type_, self.rune, self.level))

    def __str__(self):
        return self.companion.toString()

    def __repr__(self):
        return f"{type(self).__name__}({str(self)!r})"

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.type_, self.rune, self.level) == (other.type_, other.rune, other.level)

    def __bool__(self):
        return self != type(self)()

    @classmethod
    def all(cls):
        values = km.DataTypes.VYKEA_TYPE.allValues()
        return ash.to_python(values)

    @property
    def type_(self):
        return VykeaType(self.companion.getType())

    @property
    def rune(self):
        item_id = self.companion.getRune().getItemId()
        return None if item_id == types.Item.id else types.Item(item_id)

    @property
    def level(self):
        return self.companion.getLevel()

    @property
    def image(self):
        return self.companion.getImage()

    @property
    def modifiers(self):
        return self.companion.getModifiers()

    @property
    def attack_element(self):
        return types.Element(self.companion.getAttackElement().toString())
