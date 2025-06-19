#
#
from pyrogram.errors import ChannelInvalid
from pyrogram.types import Message

from strings import command
from MusicIndo import app
from MusicIndo.misc import SUDOERS, db
from MusicIndo.utils.database.memorydatabase import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)


# Function for removing the Active voice and video chat also clear the db dictionary for the chat
async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


@app.on_message(command("ACTIVEVC_COMMAND") & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("Getting Active Voicechats....\nPlease hold on")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalid:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit_text("No active Chats Found")
    else:
        await mystic.edit_text(
            f"**Active Voice Chat's:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(command("ACTIVEVIDEO_COMMAND") & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text("Getting Active Voicechats....\nPlease hold on")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalid:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit_text("No active Chats Found")
    else:
        await mystic.edit_text(
            f"**Active Video Chat's:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(command("AC_COMMAND") & SUDOERS)
async def vc(client, message: Message):
    ac_audio = str(len(await get_active_chats()))
    await message.reply_text(f"Active Chats info: {ac_audio}")
