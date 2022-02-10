import re
from collections import namedtuple
from html import escape

import pymafia.kolmafia as km
from pymafia.types import Effect, Familiar, Item, Servant, Skill

from pymafia import ash

ByteArrayOutputStream = km.autoclass("java.io.ByteArrayOutputStream")
PrintStream = km.autoclass("java.io.PrintStream")
CLICommand = namedtuple("CLICommand", ["command", "text", "status"])


def launch_gui():
    km.KoLmafia.main(["--GUI"])


def login(username, password=None):
    if password is None:
        password = km.KoLmafia.getSaveState(username)

    request = km.LoginRequest(username, password)
    request.run()
    return request


def abort(message=None):
    km.KoLmafia.updateDisplay(km.KoLConstants.MafiaState.ABORT, message)


def log(message="", html=False):
    message = str(message)
    if html is False:
        message = escape(message)

    km.RequestLogger.printLine(message)


def execute(command):
    ostream = ByteArrayOutputStream()
    ostream = km.cast("java.io.OutputStream", ostream)
    out = PrintStream(ostream)
    km.RequestLogger.openCustom(out)
    km.KoLmafiaCLI.DEFAULT_SHELL.executeLine(command)
    return CLICommand(
        command, ostream.toString(), km.NamespaceInterpreter.getContinueValue()
    )


def get_property(name, t=str):
    if t is bool:
        return km.Preferences.getBoolean(name)
    if t is int:
        return km.Preferences.getInteger(name)
    if t is float:
        return km.Preferences.getFloat(name)
    return t(km.Preferences.getString(name))


def set_property(name, value=""):
    if isinstance(value, bool):
        return km.Preferences.setBoolean(name, value)
    if isinstance(value, int):
        return km.Preferences.setInteger(name, value)
    if isinstance(value, float):
        return km.Preferences.setFloat(name, value)
    return km.Preferences.setString(name, str(value))


def force_continue():
    km.autoclass("net/sourceforge/kolmafia/KoLmafia").forceContinue()


def have(thing, quantity=1):
    if isinstance(thing, Effect):
        return ash.have_effect(thing) >= quantity
    if isinstance(thing, Familiar):
        return ash.have_familiar(thing)
    if isinstance(thing, Item):
        return ash.available_amount(thing) >= quantity
    if isinstance(thing, Servant):
        return ash.have_servant(thing)
    if isinstance(thing, Skill):
        return ash.have_skill(thing)
    raise TypeError(f"unsupported type {type(thing).__name__!r}")

def in_choice(choice):
    return ash.handling_choice() and ash.last_choice() == choice


def in_combat(monster=None):
    if ash.current_round() < 1:
        return False
    if monster is None:
        return True

    page = ash.visit_url("fight.php")
    match = re.search("<!-- MONSTERID: (\\d+) -->", page)
    if not match:
        raise RuntimeError("unable to identify monster")
    return int(match.group(1)) == monster.id


def can_kmail():
    return not (
        ash.current_round() > 0  # In a fight
        or ash.handling_choice()  # In a choice
        or ash.fight_follows_choice()  # Was in a choice, gonna be in a fight
        or ash.choice_follows_fight()  # Was in a fight, gonna be in a choice
        or ash.in_multi_fight()  # Was in a fight, gonna be in another fight
    )