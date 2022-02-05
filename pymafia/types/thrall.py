from pymafia.kolmafia import km

from pymafia import ash


class Thrall:
    def __init__(self, key):
        if key in (None, 0, "none"):
            self.id = 0
            self.name = "none"
            return

        if isinstance(key, str):
            data = km.PastaThrallData.typeToData(key)
        else:
            data = km.PastaThrallData.idToData(int(key))

        if data is None:
            raise NameError(f"{type(self).__name__} {key!r} not found")

        self.id = data[1]
        self.name = data[0]

    @classmethod
    def all(cls):
        values = km.DataTypes.THRALL_TYPE.allValues()
        return sorted(ash.from_java(values), key=lambda x: x.id)

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
        return self.id != 0
