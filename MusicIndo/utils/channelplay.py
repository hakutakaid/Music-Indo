#
#


from MusicIndo import app
from MusicIndo.utils.database import get_cmode


async def get_channeplayCB(_, command, query):
    if command == "c":
        chat_id = await get_cmode(query.message.chat.id)
        if chat_id is None:
            try:
                return await query.answer(_["setting_12"], show_alert=True)
            except Exception:
                return
        try:
            chat = await app.get_chat(chat_id)
            channel = chat.title
        except Exception:
            try:
                return await query.answer(_["cplay_4"], show_alert=True)
            except Exception:
                return
    else:
        chat_id = query.message.chat.id
        channel = None
    return chat_id, channel
