#
#
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import Message

from config import BANNED_USERS
from strings import command, get_command
from MusicIndo import app
from MusicIndo.utils.database import get_lang, set_cmode
from MusicIndo.utils.decorators.admins import AdminActual

@app.on_message(command("CHANNELPLAY_COMMAND") & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_(client, message: Message, _):
    lang_code = await get_lang(message.chat.id)
    CHANNELPLAY_COMMAND = get_command("CHANNELPLAY_COMMAND", lang_code)
    if len(message.command) < 2:
        return await message.reply_text(
            _["cplay_1"].format(message.chat.title, CHANNELPLAY_COMMAND[0])
        )
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text("Channel Play Disabled")
    elif str(query) == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                _["cplay_3"].format(chat.linked_chat.title, chat.linked_chat.id)
            )
        else:
            return await message.reply_text(_["cplay_2"])
    else:
        try:
            chat = await app.get_chat(query)
        except Exception:
            return await message.reply_text(_["cplay_4"])
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text(_["cplay_5"])
        try:
            admins = app.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            )
        except Exception:
            return await message.reply_text(_["cplay_4"])
        try:
            async for users in admins:
                if users.status == ChatMemberStatus.OWNER:
                    creatorusername = users.user.username
                    creatorid = users.user.id
        except ChatAdminRequired:
            return await message.reply_text(_["cplay_4"])

        if creatorid != message.from_user.id:
            return await message.reply_text(
                _["cplay_6"].format(chat.title, creatorusername)
            )
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(_["cplay_3"].format(chat.title, chat.id))
