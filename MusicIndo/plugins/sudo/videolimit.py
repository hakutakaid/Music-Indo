#
# Copyright (C) 2024 by hakutakaid@Github, < https://github.com/hakutakaid >.
#
# This file is part of < https://github.com/hakutakaid/MusicIndo > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/MusicIndo/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram.types import Message

from strings import command
from MusicIndo import app
from MusicIndo.misc import SUDOERS
from MusicIndo.utils.database import set_video_limit
from MusicIndo.utils.decorators.language import language


@app.on_message(command("VIDEOLIMIT_COMMAND") & SUDOERS)
@language
async def set_video_limit_kid(client, message: Message, _):
    if len(message.command) != 2:
        usage = _["vid_1"]
        return await message.reply_text(usage)
    message.chat.id
    state = message.text.split(None, 1)[1].strip()
    if state.lower() == "disable":
        limit = 0
        await set_video_limit(limit)
        return await message.reply_text(_["vid_4"])
    if state.isnumeric():
        limit = int(state)
        await set_video_limit(limit)
        if limit == 0:
            return await message.reply_text(_["vid_4"])
        await message.reply_text(_["vid_3"].format(limit))
    else:
        return await message.reply_text(_["vid_2"])
