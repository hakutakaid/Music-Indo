#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/MusicIndo > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/MusicIndo/blob/master/LICENSE >
#
# All rights reserved.

from MusicIndo.core.bot import YukkiBot
from MusicIndo.core.dir import dirr
from MusicIndo.core.git import git
from MusicIndo.core.userbot import Userbot
from MusicIndo.misc import dbb, heroku, sudo

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()

# Bot Client
app = YukkiBot()

# Assistant Client
userbot = Userbot()

from .platforms import PlaTForms

Platform = PlaTForms()
HELPABLE = {}
