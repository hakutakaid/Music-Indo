#
# Copyright (C) 2024 by hakutakaid@Github, < https://github.com/hakutakaid >.
#
# This file is part of < https://github.com/hakutakaid/MusicIndo > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/MusicIndo/blob/master/LICENSE >
#
# All rights reserved.
#


import config
from strings import command
from MusicIndo import app
from MusicIndo.misc import SUDOERS
from MusicIndo.utils.database import add_off, add_on
from MusicIndo.utils.decorators.language import language


@app.on_message(command("LOGGER_COMMAND") & SUDOERS)
@language
async def logger(client, message, _):
    usage = _["log_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await add_on(config.LOG)
        await message.reply_text(_["log_2"])
    elif state == "disable":
        await add_off(config.LOG)
        await message.reply_text(_["log_3"])
    else:
        await message.reply_text(usage)
