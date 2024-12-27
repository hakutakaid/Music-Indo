#
#Hakutakaid
#
#
#

from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import LOG_GROUP_ID
from config import BANNED_USERS
from strings import command
from ChiefMusic import app
from ChiefMusic.core.call import Yukki
from ChiefMusic.utils.decorators.play import PlayWrapper
from ChiefMusic.utils.logger import play_logs
from ChiefMusic.utils.stream.stream import stream


@app.on_message(command("STREAM_COMMAND") & filters.group & ~BANNED_USERS)
@PlayWrapper
async def stream_command(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    if url:
        mystic = await message.reply_text(
            _["play_2"].format(channel) if channel else _["play_1"]
        )
        try:
            await Yukki.stream_call(url)
        except NoActiveGroupCall:
            await mystic.edit_text(
                "There's an issue with the bot. please report it to my Owner and ask them to check logger group"
            )
            text = "Please Turn on voice chat.. Bot is unable to stream urls.."
            return await app.send_message(int(LOG_GROUP_ID), text)
        except Exception as e:
            return await mystic.edit_text(_["general_3"].format(type(e).__name__))
        await mystic.edit_text(_["str_2"])
        try:
            await stream(
                _,
                mystic,
                message.from_user.id,
                url,
                chat_id,
                message.from_user.first_name,
                message.chat.id,
                video=True,
                streamtype="index",
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            return await mystic.edit_text(err)
        return await play_logs(message, streamtype="M3u8 or Index Link")
    else:
        await message.reply_text(_["str_1"])
