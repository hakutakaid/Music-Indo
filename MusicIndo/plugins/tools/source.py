from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from MusicIndo import app
from config import SUPPORT_CHANNEL, SUPPORT_GROUP
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from pyrogram.enums import ChatMemberStatus


@app.on_callback_query(filters.regex("source_code"))
async def gib_repo_callback(_, callback_query):
    if app.username == "ManageMusic_Bot":
        try:
            get = await app.get_chat_member(-1001705041312, callback_query.from_user.id)
        except ChatAdminRequired:
            return await callback_query.message.edit(
                "Support chat",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʙᴀᴄᴋ", callback_data="settingsback_helper"
                            ),
                            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close"),
                        ]
                    ]
                ),
            )
        except UserNotParticipant:
            return await callback_query.message.edit(
                "Channels Support",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=SUPPORT_CHANNEL),
                            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close"),
                        ]
                    ]
                ),
            )
#         if get.status == ChatMemberStatus.LEFT:
#             return await callback_query.message.edit(
#                 "Bantu support dengan join ke Channels atau group",
#                 reply_markup=InlineKeyboardMarkup(
#                     [
#                         [
#                             InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=SUPPORT_CHANNEL),
#                             InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close"),
#                         ]
#                     ]
#                 ),
#             )
#         else:
#             return await callback_query.message.edit(
#                 "Are you asking about repo? If you want to ask about the repo, please ask by contacting my developer [Developer](https://t.me/Usern4meDoesNotExist404)",
#                 disable_web_page_preview=True,
#                 reply_markup=InlineKeyboardMarkup(
#                     [
#                         [
#                             InlineKeyboardButton(text="ɢʀᴏᴜᴘ", url=SUPPORT_GROUP),
#                             InlineKeyboardButton(
#                                 text="ʙᴀᴄᴋ", callback_data="settingsback_helper"
#                             ),
#                         ]
#                     ]
#                 ),
#             )
# 
