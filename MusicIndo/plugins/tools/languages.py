#
#

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from config import BANNED_USERS
from strings import command, get_string, languages_present
from MusicIndo import app
from MusicIndo.utils.database import get_lang, set_lang
from MusicIndo.utils.decorators import ActualAdminCB, language, languageCB

# Languages Available


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                InlineKeyboardButton(
                    text=languages_present[i],
                    callback_data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard


@app.on_message(command("LANGUAGE_COMMAND") & filters.group & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, query, _):
    try:
        await query.answer()
    except Exception:
        pass
    keyboard = lanuages_keyboard(_)
    return await query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, query, _):
    langauge = (query.data).split(":")[1]
    old = await get_lang(query.message.chat.id)
    if str(old) == str(langauge):
        return await query.answer(
            "You are already using the same language", show_alert=True
        )
    try:
        _ = get_string(langauge)
        await query.answer("Your language changed successfully..", show_alert=True)
    except Exception:
        return await query.answer(
            "Failed to change language or language is under maintenance",
            show_alert=True,
        )
    await set_lang(query.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await query.edit_message_reply_markup(reply_markup=keyboard)
