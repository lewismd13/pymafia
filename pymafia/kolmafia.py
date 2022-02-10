import json
import os
import re
import zipfile
from urllib import request

import jnius_config
import wrapt

JAR_LOCATION = "./kolmafia.jar"
JENKINS_JOB_URL = "https://ci.kolmafia.us/job/Kolmafia/lastSuccessfulBuild/"
JAVA_PATTERN = "(net\\/sourceforge\\/kolmafia.*\\/([^\\$]*))\\.class"


class MafiaError(Exception):
    pass


def unproxy(obj):
    """Extract the wrapped object from an proxy."""
    if isinstance(obj, wrapt.ObjectProxy):
        return object.__getattribute__(obj, "__wrapped__")
    return obj


@wrapt.decorator
def monitor(wrapped, instance, args, kwargs):  # pylint: disable=W0613
    """Execute a callable and check mafia for errors.
    Wrap the callable result with a proxy if it is a jnius object
    """
    result = wrapped(*args, **kwargs)

    if not autoclass("net/sourceforge/kolmafia/KoLmafia").permitsContinue():
        raise MafiaError(
            autoclass("net/sourceforge/kolmafia/KoLmafia").getLastMessage()
        )

    if type(result).__module__.split(".")[0] == "jnius":
        return JniusCallableProxy(result) if callable(result) else JniusProxy(result)

    return result


class JniusProxy(wrapt.ObjectProxy):  # pylint: disable=W0223
    """Proxy a non-callable jnius objects and monitor mafia for errors.
    Specifying a __call__ method for non-callable jnius objects results in a jnius conversion error.
    """

    @monitor
    def __getattribute__(self, name):
        return super().__getattribute__(name)


class JniusCallableProxy(JniusProxy):  # pylint: disable=W0223
    """Proxy a callable jnius objects and monitor mafia for errors."""

    @monitor
    def __call__(self, *args, **kwargs):
        args = [unproxy(item) for item in args]
        kwargs = {k: unproxy(v) for k, v in kwargs.items()}
        return object.__getattribute__(self, "__wrapped__")(*args, **kwargs)


@monitor
def __getattr__(key):
    return autoclass(classes[key]) if key in classes else autoclass(key)


def download(location):
    with request.urlopen(JENKINS_JOB_URL + "/api/json") as response:
        data = json.loads(response.read().decode())
        jar_url = JENKINS_JOB_URL + "artifact/" + data["artifacts"][0]["relativePath"]
        request.urlretrieve(jar_url, filename=location)


if not os.path.isfile(JAR_LOCATION):
    download(JAR_LOCATION)
jnius_config.set_classpath(JAR_LOCATION)
from jnius import autoclass, cast  # pylint: disable=C,E,W

classes = {}
with zipfile.ZipFile(JAR_LOCATION) as archive:
    for file in archive.filelist:
        filename = file.orig_filename
        match = re.search(JAVA_PATTERN, filename)
        if match:
            classes[match.group(2)] = match.group(1)
