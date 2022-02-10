import pymafia.kolmafia as km

from pymafia import ash


class Servant:
    def __init__(self, key):
        if key in (None, 0, "none"):
            self.data = None
            return

        data = (
            km.EdServantData.typeToData(key)
            if isinstance(key, str)
            else km.EdServantData.idToData(key)
        )

        if data is None:
            raise NameError(f"{type(self).__name__} {key!r} not found")

        self.data = data

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{type(self).__name__}({str(self)!r})"

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.id, self.name) == (
            other.id,
            other.name,
        )

    def __bool__(self):
        return self.data is not None

    @classmethod
    def all(cls):
        values = km.DataTypes.SERVANT_TYPE.allValues()
        return sorted(ash.to_python(values), key=lambda x: x.id)

    @property
    def id(self):
        return self.data[2] if self else 0

    @property
    def name(self):
        return self.data[0] if self else "none"

    @property
    def level(self):
        servant = km.EdServantData.findEdServant(self.name)
        return 0 if servant is None else servant.getLevel()

    @property
    def experience(self):
        servant = km.EdServantData.findEdServant(self.name)
        return 0 if servant is None else servant.getExperience()

    @property
    def image(self):
        return self.data[3] if self else None

    @property
    def level1_ability(self):
        return self.data[4] if self else None

    @property
    def level7_ability(self):
        return self.data[5] if self else None

    @property
    def level14_ability(self):
        return self.data[6] if self else None

    @property
    def level21_ability(self):
        return self.data[7] if self else None
