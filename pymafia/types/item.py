from enum import Enum
from functools import cached_property

from pymafia.kolmafia import km

from pymafia import ash


class ItemQuality(Enum):
    NONE = ""
    CRAPPY = "crappy"
    DECENT = "decent"
    GOOD = "good"
    AWESOME = "awesome"
    EPIC = "EPIC"


class CandyType(Enum):
    NONE = "none"
    UNSPADED = "unspaded"
    SIMPLE = "simple"
    COMPLEX = "complex"


class Item:
    def __init__(self, key):
        if key in (None, -1, "none"):
            self.id = -1
            self.name = "none"
            return

        id_ = int(km.ItemDatabase.getItemId(key) if isinstance(key, str) else key)
        name = km.ItemDatabase.getDisplayName(id_)

        if name is None:
            raise NameError(f"{type(self).__name__} {key!r} not found")

        self.id = id_
        self.name = name

    @classmethod
    def all(cls):
        values = km.DataTypes.ITEM_TYPE.allValues()
        return ash.to_python(values)

    def __int__(self):
        return self.id

    def __hash__(self):
        return hash((self.id, self.name))

    def __str__(self):
        return f"[{self.id}]{self.name}" if self else self.name

    def __repr__(self):
        return f"{type(self).__name__}({str(self)!r})"

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.id, self.name) == (
            other.id,
            other.name,
        )

    def __bool__(self):
        return self.id != -1

    @cached_property
    def plural(self):
        """Return the plural of the Item. If the official plural is not known, return the name of the Item with an "s" appended."""
        return km.ItemDatabase.getPluralName(self.id)

    @cached_property
    def descid(self):
        """Return the descid of the Item. This is the identifier used to see the description of the Item."""
        return km.ItemDatabase.getDescriptionId(self.id)

    @cached_property
    def image(self):
        """Return the filename of the image associated with the Item."""
        return km.ItemDatabase.getImage(self.id)

    @cached_property
    def smallimage(self):
        """Returns the filename of the small image associated with the Item. For items with an image that is usually larger than 30x30, returns their 30x30 equivalent.

        For example, "folders" from the "over-the-shoulder Folder Holder" will normally return a 100x100 image but a 30x30 image here.
        """
        return km.ItemDatabase.getSmallImage(self.id)

    @cached_property
    def levelreq(self):
        """Return the level requirement for consuming or equipping the Item."""
        return km.ConsumablesDatabase.getLevelReqByName(self.name)

    @cached_property
    def quality(self):
        """Return the quality of the Item if it is a consumable."""
        return ItemQuality(km.ConsumablesDatabase.getQuality(self.name))

    @cached_property
    def adventures(self):
        """Return the range of adventures gained from consuming the Item. The string will either contain the adventures for invariant gains, or a hyphen-separated minimum and maximum for variant gains."""
        return km.ConsumablesDatabase.getAdvRangeByName(self.name)

    @cached_property
    def muscle(self):
        """Return the range of muscle substats gained from consuming the Item. The string will either contain the substats for invariant gains, or a hyphen-separated minimum and maximum for variant gains. Note that substat gains can be negative."""
        return km.ConsumablesDatabase.getMuscleByName(self.name)

    @cached_property
    def mysticality(self):
        """Return the range of mysticality substats gained from consuming the Item. The string will either contain the substats for invariant gains, or a hyphen-separated minimum and maximum for variant gains. Note that substat gains can be negative."""
        return km.ConsumablesDatabase.getMysticalityByName(self.name)

    @cached_property
    def moxie(self):
        """Return the range of moxie substats gained from consuming the Item. The string will either contain the substats for invariant gains, or a hyphen-separated minimum and maximum for variant gains. Note that substat gains can be negative."""
        return km.ConsumablesDatabase.getMoxieByName(self.name)

    @cached_property
    def fullness(self):
        """Return the stomach size of Item. If the Item is not edible, return 0."""
        return km.ConsumablesDatabase.getFullness(self.name)

    @cached_property
    def inebriety(self):
        """Return the liver size of Item. If the Item is not drinkable, return 0."""
        return km.ConsumablesDatabase.getInebriety(self.name)

    @cached_property
    def spleen(self):
        """Return the spleen size of Item. If the Item is not chewable, return 0."""
        return km.ConsumablesDatabase.getSpleenHit(self.name)

    @cached_property
    def minhp(self):
        """Return the minimum HP restored by consuming this Item."""
        return km.RestoresDatabase.getHPMin(self.name)

    @cached_property
    def maxhp(self):
        """Return the maximum HP restored by consuming this Item."""
        return km.RestoresDatabase.getHPMax(self.name)

    @cached_property
    def minmp(self):
        """Return the minimum MP restored by consuming this Item."""
        return km.RestoresDatabase.getMPMin(self.name)

    @cached_property
    def maxmp(self):
        """Return the maximum MP restored by consuming this Item."""
        return km.RestoresDatabase.getMPMax(self.name)

    @cached_property
    def dailyusesleft(self):
        """Return the number of daily uses remaining for this Item."""
        return km.UseItemRequest.maximumUses(self.id)

    @cached_property
    def notes(self):
        """Return any notes that exist for the Item. Examples of (comma-separated) contents are:

        - The name and duration of any effects granted by consumption, if applicable.
        - Items dropped when the item is consumed, if applicable.
        - Tags relevant to game mechanics (such as "MARTINI", "BEER" and "SAUCY")
        - "Unspaded"
        """
        return km.ConsumablesDatabase.getNotes(self.name)

    @cached_property
    def quest(self):
        """Return True if the Item is a quest item, else False."""
        return km.ItemDatabase.isQuestItem(self.id)

    @cached_property
    def gift(self):
        """Return True if the Item is a gift item, else False."""
        return km.ItemDatabase.isGiftItem(self.id)

    @cached_property
    def tradeable(self):
        """Return True if the Item is tradeable, else False."""
        return km.ItemDatabase.isTradeable(self.id)

    @cached_property
    def discardable(self):
        """Return True if the Item is discardable, else False."""
        return km.ItemDatabase.isDiscardable(self.id)

    @cached_property
    def combat(self):
        """Return True if the Item is usable in combat, else False. This returns True whether the Item is consumed by being used or not."""
        return km.ItemDatabase.getAttribute(
            self.id, km.ItemDatabase.ATTR_COMBAT | km.ItemDatabase.ATTR_COMBAT_REUSABLE
        )

    @cached_property
    def combat_reusable(self):
        """Return True if the Item is usable in combat and is not consumed when doing so, else False."""
        return km.ItemDatabase.getAttribute(
            self.id, km.ItemDatabase.ATTR_COMBAT_REUSABLE
        )

    @cached_property
    def usable(self):
        """Return True if the Item is usable, else False. This returns True whether the Item is consumed by being used or not."""
        return km.ItemDatabase.isUsable(self.id)

    @cached_property
    def reusable(self):
        """Return True if the Item is usable and is not consumed when doing so, else False."""
        return km.ItemDatabase.getConsumptionType(
            self.id
        ) == km.KoLConstants.INFINITE_USES or km.ItemDatabase.getAttribute(
            self.id, km.ItemDatabase.ATTR_REUSABLE
        )

    @cached_property
    def multi(self):
        """Return True if the Item is multiusable, else False."""
        return km.ItemDatabase.isMultiUsable(self.id)

    @cached_property
    def fancy(self):
        """Return True if the Item is a "fancy" ingredient, else False."""
        return km.ItemDatabase.isFancyItem(self.id)

    @cached_property
    def pasteable(self):
        """Return True if the Item is a meatpasting ingredient, else False."""
        return km.ItemDatabase.isPasteable(self.id)

    @cached_property
    def smithable(self):
        """Return True if the Item is a meatsmithing ingredient, else False."""
        return km.ItemDatabase.isSmithable(self.id)

    @cached_property
    def cookable(self):
        """Return True if the Item is a cooking ingredient, else False."""
        return km.ItemDatabase.isCookable(self.id)

    @cached_property
    def mixable(self):
        """Return True if the Item is a cocktailcrafting ingredient, else False."""
        return km.ItemDatabase.isMixable(self.id)

    @cached_property
    def candy(self):
        """Return True if the Item is a candy, else False."""
        return km.ItemDatabase.isCandyItem(self.id)

    @cached_property
    def candy_type(self):
        """Return the candy type of the Item."""
        return CandyType(km.CandyDatabase.getCandyType(self.id))

    @cached_property
    def chocolate(self):
        """Return True if the Item is a chocolate, else False."""
        return km.ItemDatabase.isChocolateItem(self.id)

    @cached_property
    def seller(self):
        """Return which Coinmaster sells this Item, if any."""
        return ash.to_python(
            km.DataTypes.makeCoinmasterValue(km.CoinmasterRegistry.findSeller(self.id))
        )

    @cached_property
    def buyer(self):
        """Return which Coinmaster buys this Item, if any."""
        return ash.to_python(
            km.DataTypes.makeCoinmasterValue(km.CoinmasterRegistry.findBuyer(self.id))
        )

    @cached_property
    def name_length(self):
        """Return the length of the Item's display name."""
        return km.ItemDatabase.getNameLength(self.id)

    @cached_property
    def noob_skill(self):
        """Return the noob Skill granted by absorbing this Item."""
        return ash.to_python(
            km.DataTypes.makeSkillValue(km.ItemDatabase.getNoobSkillId(self.id), True)
        )

    @property
    def tcrs_name(self):
        """Return the name of the Item as it appears in your current Two Crazy Random Summer run. If you are not in a TCRS run, the regular Item name is returned."""
        return km.TCRSDatabase.getTCRSName(self.id)
