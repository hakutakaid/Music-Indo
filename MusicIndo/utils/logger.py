#

from config import LOG, LOG_GROUP_ID
from strings import get_string
from MusicIndo import app
from MusicIndo.utils.database import get_lang, is_on_off


async def play_logs(message, streamtype):
    if await is_on_off(LOG):
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except Exception:
            _ = get_string("en")

        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "Private Group"

        if message.from_user.username:
            username = f"@{message.from_user.username}"
        else:
            username = "Unknow"

        if message.reply_to_message:
            query = "Replied Message"
        else:
            query = message.text.split(None, 1)[1]

        logger_text = _["logger_text"].format(
            bot_mention=app.mention,
            chat_id=message.chat.id,
            title=message.chat.title,
            chatusername=chatusername,
            sender_id=message.from_user.id,
            user_mention=message.from_user.mention,
            username=username,
            query=query,
            streamtype=streamtype,
        )
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(e)
        return
