#
# Copyright (C) 2024 by hakutakaid@Github, < https://github.com/hakutakaid >.
#
# This file is part of < https://github.com/hakutakaid/MusicIndo > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/MusicIndo/blob/master/LICENSE >
#
# All rights reserved.
#


from MusicIndo import app
from MusicIndo.utils.database import get_cmode


async def get_channeplayCB(_, command, CallbackQuery):
    if command == "c":
        chat_id = await get_cmode(CallbackQuery.message.chat.id)
        if chat_id is None:
            try:
                return await CallbackQuery.answer(_["setting_12"], show_alert=True)
            except Exception:
                return
        try:
            chat = await app.get_chat(chat_id)
            channel = chat.title
        except Exception:
            try:
                return await CallbackQuery.answer(_["cplay_4"], show_alert=True)
            except Exception:
                return
    else:
        chat_id = CallbackQuery.message.chat.id
        channel = None
    return chat_id, channel
