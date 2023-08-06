"""
dpy-utils
~~~~~~~~~~~~~~~~~~~
a collection of utils I use with discord.py
"""

__description__ = "a collection of utils I use with discord.py"
__version__ = "0.0.1a"

from typing import Literal, NamedTuple

from .abc import *
from .bot import *
from .converters import *
from .extra import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str


raw_version = __version__.split(".")
try:
    raw_release_releaselevel = {"a": "alpha", "b": "beta", "c": "candidate"}.get(
        raw_version[2][1], "final"
    )
except IndexError:
    raw_release_releaselevel = "final"
version_info = VersionInfo(
    major=int(raw_version[0]),
    minor=int(raw_version[1]),
    micro=int(raw_version[2][0]),
    releaselevel=raw_release_releaselevel,
)

del Literal, NamedTuple, VersionInfo, raw_release_releaselevel, raw_version
