import sys
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand
import config

from ..logging import LOGGER


class RynBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "MusicIndo",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                text=f"<blockquote><b>{self.mention} Bot dimulai :</b><u>\n\nId : <code>{self.id}</code>\nName : {self.name}\nUsername : @{self.username} </b></blockquote>",
            )
        except:
            LOGGER(__name__).error(
                "Bot has failed to access the log Group. Make sure that you have added your bot to your log channel and promoted as admin!"
            )
            sys.exit()
        if config.SET_CMDS:
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("start", "📚 mulai Bot"),
                        BotCommand("ping", "📈 cek apakah bot mati atau hidup"),
                        BotCommand("play", "🗒️ mainkan music"),
                        BotCommand("q", "🤖 Buat stcikers"),
                        BotCommand("kang", "💾 Save stcikers replay"),
                        BotCommand("skip", "🎙️ putar lagu selanjutnya "),
                        BotCommand("pause", "⚠️ hentikan music sementara"),
                        BotCommand("resume", "🎭 resume music"),
                        BotCommand("end", "🎙️ matikan music"),
                        BotCommand(
                            "playmode",
                            "🤖 pengaturan play music",
                        ),
                        BotCommand(
                            "settings",
                            "☎️ pengaturan bot",
                        ),
                    ]
                )
            except:
                pass
        else:
            pass
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error("Tolong promosikan bot sebagai admin di log group")
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"MusicIndo Dimulai {self.name}")
