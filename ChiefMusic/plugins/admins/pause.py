#
#Hakutakaid
#
#
#

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import command
from ChiefMusic import app
from ChiefMusic.core.call import Yukki
from ChiefMusic.utils.database import is_music_playing, music_off
from ChiefMusic.utils.decorators import AdminRightsCheck


@app.on_message(command("PAUSE_COMMAND") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await Yukki.pause_stream(chat_id)
    await message.reply_text(_["admin_2"].format(message.from_user.mention))
