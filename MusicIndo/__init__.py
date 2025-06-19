#
import asyncio as _asyncio

import uvloop as _uvloop

_asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())  # noqa

from MusicIndo.core.bot import YukkiBot
from MusicIndo.core.dir import dirr
from MusicIndo.core.git import git
from MusicIndo.core.userbot import Userbot
from MusicIndo.misc import dbb, heroku

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

app = YukkiBot()
userbot = Userbot()

HELPABLE = {}
