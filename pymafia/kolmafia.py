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


class JniusProxy(wrapt.ObjectProxy):  # pylint: disable=W0223
    """Wrapper for jnius objects that monitors KoLmafia for errors."""

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)

        if not object.__getattribute__(self, "permits_continue"):
            raise MafiaError(object.__getattribute__(self, "last_message"))

        if type(attr).__module__.startswith("jnius"):
            return type(self)(attr)
        return attr

    def __call__(self, *args, **kwargs):
        result = object.__getattribute__(self, "__wrapped__")(*args, **kwargs)

        if not object.__getattribute__(self, "permits_continue"):
            raise MafiaError(object.__getattribute__(self, "last_message"))

        if type(result).__module__.startswith("jnius"):
            return type(self)(result)
        return result

    @property
    def permits_continue(self):
        return autoclass("net/sourceforge/kolmafia/KoLmafia").permitsContinue()

    @property
    def last_message(self):
        return autoclass("net/sourceforge/kolmafia/KoLmafia").getLastMessage()


def __getattr__(key):
    return JniusProxy(autoclass(classes[key]) if key in classes else autoclass(key))


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
