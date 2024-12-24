#
# Copyright (C) 2024 by hakutakaid@Github, < https://github.com/hakutakaid >.
#
# This file is part of < https://github.com/hakutakaid/MusicIndo > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/MusicIndo/blob/master/LICENSE >
#
# All rights reserved.
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from MusicIndo import HELPABLE, LOGGER, app, userbot
from MusicIndo.core.call import Yukki
from MusicIndo.plugins import ALL_MODULES
from MusicIndo.utils.database import get_banned_users, get_gbanned


async def init():
    if len(config.STRING_SESSIONS) == 0:
        LOGGER("MusicIndo").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("MusicIndo").warning(
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
    LOGGER("MusicIndo.plugins").info("Successfully Imported All Modules ")
    await userbot.start()
    await Yukki.start()
    LOGGER("MusicIndo").info("Assistant Started Sucessfully")
    try:
        await Yukki.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("MusicIndo").error(
            "Please ensure the voice call in your log group is active."
        )
        exit()

    await Yukki.decorators()
    LOGGER("MusicIndo").info("MusicIndo Started Successfully")
    await idle()
    await app.stop()
    await userbot.stop()


if __name__ == "__main__":
    app.run(init())
    LOGGER("MusicIndo").info("Stopping MusicIndo! GoodBye")
