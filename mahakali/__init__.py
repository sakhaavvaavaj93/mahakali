from mahakali.core.bot import Dil
from mahakali.core.dir import dirr
from mahakali.core.git import git
from mahakali.core.userbot import Userbot
from mahakali.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Dil()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
