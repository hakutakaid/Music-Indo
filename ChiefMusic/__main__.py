#
#Hakutakaid
#
#
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from ChiefMusic import HELPABLE, LOGGER, app, userbot
from ChiefMusic.core.call import Yukki
from ChiefMusic.plugins import ALL_MODULES
from ChiefMusic.utils.database import get_banned_users, get_gbanned


async def init():
    if len(config.STRING_SESSIONS) == 0:
        LOGGER("ChiefMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("ChiefMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("ChiefMusic.plugins").info("Successfully Imported All Modules ")
    await userbot.start()
    await Yukki.start()
    LOGGER("ChiefMusic").info("Assistant Started Sucessfully")
    try:
        await Yukki.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("ChiefMusic").error(
            "Please ensure the voice call in your log group is active."
        )
        exit()

    await Yukki.decorators()
    LOGGER("ChiefMusic").info("ChiefMusic Started Successfully")
    await idle()
    await app.stop()
    await userbot.stop()


if __name__ == "__main__":
    app.run(init())
    LOGGER("ChiefMusic").info("Stopping ChiefMusic! GoodBye")
