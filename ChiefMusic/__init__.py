#
#Hakutakaid
#
#

from ChiefMusic.core.bot import YukkiBot
from ChiefMusic.core.dir import dirr
from ChiefMusic.core.git import git
from ChiefMusic.core.userbot import Userbot
from ChiefMusic.misc import dbb, heroku, sudo

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
