from pymafia import ash, get_property, have as _have, Item

item = Item("SongBoom™ BoomBox")

song_keywords = {
    "Eye of the Giger": "spooky",
    "Food Vibrations": "food",
    "Remainin' Alive": "dr",
    "These Fists Were Made for Punchin'": "damage",
    "Total Eclipse of Your Meat": "meat",
    "Silence": "off",
    None: "off",
}


def have():
    return _have(item)


def song():
    """Current song."""
    return get_property("boomBoxSong") or None


def song_changes_left():
    """Song changes left today."""
    return get_property("_boomBoxSongsLeft", int)


def set_song(new_song):
    """Change the song."""
    if not have():
        raise RuntimeError("need a SongBoom™ BoomBox")
    if song() == new_song:
        return
    if song_changes_left() < 1:
        raise RuntimeError("out of song changes")

    success = ash.cli_execute(f"boombox {song_keywords[new_song]}")

    if not success:
        raise RuntimeError(f"failed to set song to {new_song!r}")


def drop_progress():
    """Progress to next song drop (e.g. gathered meat-clip)."""
    return get_property("_boomBoxFights", int)
