from SafoneAPI import SafoneAPI
from MusicIndo.core.bot import RynBot
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
api = SafoneAPI()
# Bot Client
app = RynBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
HELPABLE = {}
