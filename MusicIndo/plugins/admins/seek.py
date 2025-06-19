#
#
from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import command
from MusicIndo import app
from MusicIndo.core.call import Yukki
from MusicIndo.misc import db
from MusicIndo.platforms import youtube
from MusicIndo.utils import AdminRightsCheck, seconds_to_min


@app.on_message(
    command(["SEEK_COMMAND", "SEEK_BACK_COMMAND"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def seek_comm(cli, message: Message, _, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(_["admin_28"])
    query = message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        return await message.reply_text(_["admin_29"])
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["admin_30"])
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return await message.reply_text(_["admin_30"])
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if message.command[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            return await message.reply_text(
                _["admin_31"].format(seconds_to_min(duration_played), duration)
            )
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            return await message.reply_text(
                _["admin_31"].format(seconds_to_min(duration_played), duration)
            )
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text(_["admin_32"])
    if "vid_" in file_path:
        n, file_path = await youtube.video(playing[0]["vidid"], True)
        if n == 0:
            return await message.reply_text(_["admin_30"])
    try:
        await Yukki.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except Exception:
        return await mystic.edit_text(_["admin_34"])
    if message.command[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text(_["admin_33"].format(seconds_to_min(to_seek)))
