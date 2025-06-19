#
#
import asyncio
import logging
import traceback

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChannelsTooMuch,
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, filters
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import (
    ChatUpdate,
    GroupCallConfig,
    MediaStream,
    StreamEnded,
)

import config
from strings import get_string
from MusicIndo import app, userbot
from MusicIndo.core.userbot import assistants
from MusicIndo.misc import db
from MusicIndo.platforms import saavn, youtube
from MusicIndo.utils import fallback
from MusicIndo.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_active_chats,
    get_assistant,
    get_audio_bitrate,
    get_lang,
    get_loop,
    get_video_bitrate,
    group_assistant,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_assistant,
    set_loop,
)
from MusicIndo.utils.exceptions import AssistantErr
from MusicIndo.utils.inline.play import stream_markup, telegram_markup
from MusicIndo.utils.stream.autoclear import auto_clean
from MusicIndo.utils.thumbnails import gen_thumb

links = {}
logger = logging.getLogger(__name__)


async def _clear_(chat_id):
    popped = db.pop(chat_id, None)
    if popped:
        await auto_clean(popped)
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)
    await set_loop(chat_id, 0)


class Call:
    def __init__(self):
        self.calls = []

        for client in userbot.clients:
            pycall = PyTgCalls(
                client,
                cache_duration=100,
            )
            self.calls.append(pycall)

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume(chat_id)

    async def mute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.mute(chat_id)

    async def unmute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.unmute(chat_id)

    async def leave_call(self, chat_id):
        assistant = await group_assistant(self, chat_id)
        await assistant.leave_call(chat_id)

    async def stop_stream(self, chat_id: int):
        try:
            await _clear_(chat_id)
            await self.leave_call(chat_id)
        except Exception:
            pass

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except Exception:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_call(chat_id)
        except Exception:
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: bool | str = None,
        image: bool | str = None,
    ):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        call_config = GroupCallConfig(auto_start=False)
        if video:
            stream = MediaStream(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
        elif image and config.PRIVATE_BOT_MODE:
            stream = MediaStream(
                image,
                audio_path=link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
        else:
            stream = MediaStream(
                link,
                audio_parameters=audio_stream_quality,
                video_flags=MediaStream.Flags.IGNORE,
            )

        await assistant.play(chat_id, stream, config=call_config)

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        call_config = GroupCallConfig(auto_start=False)
        stream = (
            MediaStream(
                file_path,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode == "video"
            else MediaStream(
                file_path,
                audio_parameters=audio_stream_quality,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
                video_flags=MediaStream.Flags.IGNORE,
            )
        )
        await assistant.play(chat_id, stream, config=call_config)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        call_config = GroupCallConfig(auto_start=False)
        await assistant.play(
            config.LOG_GROUP_ID,
            MediaStream(link),
            config=call_config,
        )
        await asyncio.sleep(0.5)
        await assistant.leave_call(config.LOG_GROUP_ID)

    async def join_chat(self, chat_id, attempts=1):
        max_attempts = len(assistants) - 1
        userbot = await get_assistant(chat_id)
        try:
            language = await get_lang(chat_id)
            _ = get_string(language)
        except Exception:
            _ = get_string("en")
        try:
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                raise AssistantErr(_["call_1"])
            if get.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
                try:
                    await app.unban_chat_member(chat_id, userbot.id)
                except Exception:
                    raise AssistantErr(_["call_2"].format(userbot.username, userbot.id))
        except UserNotParticipant:
            pass
        try:
            chat = await app.get_chat(chat_id)
        except ChatAdminRequired:
            raise AssistantErr(_["call_1"])
        except Exception as e:
            raise AssistantErr(_["call_3"].format(app.mention, type(e).__name__))
        if chat_id in links:
            invitelink = links[chat_id]
        else:
            if chat.username:
                invitelink = chat.username
                try:
                    await userbot.resolve_peer(invitelink)
                except Exception:
                    pass
            else:
                try:
                    invitelink = await app.export_chat_invite_link(chat_id)
                except ChatAdminRequired:
                    raise AssistantErr(_["call_1"])
                except Exception as e:
                    raise AssistantErr(
                        _["call_3"].format(app.mention, type(e).__name__)
                    )

            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            links[chat_id] = invitelink

        try:
            await asyncio.sleep(1)
            await userbot.join_chat(invitelink)
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(chat_id, userbot.id)
            except Exception as e:
                raise AssistantErr(_["call_3"].format(type(e).__name__))
            await asyncio.sleep(1)
            # raise AssistantErr(_["call_6"].format(app.mention))
        except UserAlreadyParticipant:
            pass
        except ChannelsTooMuch:
            if attempts <= max_attempts:
                attempts += 1
                userbot = await set_assistant(chat_id)
                return await self.join_chat(chat_id, attempts)
            else:
                raise AssistantErr(_["call_9"].format(config.SUPPORT_GROUP))
        except FloodWait as e:
            time = e.value
            if time < 20:
                await asyncio.sleep(time)
                attempts += 1
                return await self.join_chat(chat_id, attempts)
            else:
                if attempts <= max_attempts:
                    attempts += 1
                    userbot = await set_assistant(chat_id)
                    return await self.join_chat(chat_id, attempts)

                raise AssistantErr(_["call_10"].format(time))
        except Exception as e:
            raise AssistantErr(_["call_3"].format(type(e).__name__))

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: bool | str = None,
        image: bool | str = None,
    ):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        call_config = GroupCallConfig(auto_start=False)
        if video:
            stream = MediaStream(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
        elif image and config.PRIVATE_BOT_MODE:
            stream = MediaStream(
                image,
                audio_path=link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
        else:
            stream = MediaStream(
                link,
                audio_parameters=audio_stream_quality,
                video_flags=MediaStream.Flags.IGNORE,
            )

        try:
            await assistant.play(
                chat_id,
                stream=stream,
                config=call_config,
            )
        except Exception:
            traceback.print_exc()
            await self.join_chat(chat_id)
            try:
                await assistant.play(
                    chat_id,
                    stream=stream,
                    config=call_config,
                )
            except Exception:
                traceback.print_exc()
                raise AssistantErr(
                    "**No Active Voice Chat Found**\n\nPlease make sure group's voice chat is enabled. If already enabled, please end it and start fresh voice chat again and if the problem continues, try /restart"
                )

        except NoActiveGroupCall:
            raise AssistantErr(
                "**No Active Voice Chat Found**\n\nPlease make sure group's voice chat is enabled. If already enabled, please end it and start fresh voice chat again and if the problem continues, try /restart"
            )
        except TelegramServerError:
            raise AssistantErr(
                "**TELEGRAM SERVER ERROR**\n\nPlease restart Your voicechat."
            )
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            if popped:
                await auto_clean(popped)
                if popped.get("mystic"):
                    try:
                        await popped.get("mystic").delete()
                    except Exception:
                        pass
            if not check:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
        except Exception:
            try:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
            except Exception:
                return
        else:
            queued = check[0]["file"]
            language = await get_lang(chat_id)
            _ = get_string(language)
            title = (check[0]["title"]).title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]
            audio_stream_quality = await get_audio_bitrate(chat_id)
            video_stream_quality = await get_video_bitrate(chat_id)
            videoid = check[0]["vidid"]
            check[0].get("user_id")
            check[0]["played"] = 0
            video = True if str(streamtype) == "video" else False
            call_config = GroupCallConfig(auto_start=False)
            if "live_" in queued:
                n, link = await youtube.video(videoid, True)
                if n == 0:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
                    )
                if video:
                    stream = MediaStream(
                        link,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    try:
                        image = await youtube.thumbnail(videoid, True)
                    except Exception:
                        image = None
                    if image and config.PRIVATE_BOT_MODE:
                        stream = MediaStream(
                            image,
                            audio_path=link,
                            audio_parameters=audio_stream_quality,
                            video_parameters=video_stream_quality,
                        )
                    else:
                        stream = MediaStream(
                            link,
                            audio_parameters=audio_stream_quality,
                            video_flags=MediaStream.Flags.IGNORE,
                        )
                try:
                    await client.play(chat_id, stream, config=call_config)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
                    )
                img = await gen_thumb(videoid)
                button = telegram_markup(_, chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif "vid_" in queued:
                mystic = await app.send_message(original_chat_id, _["call_8"])
                flink = f"https://t.me/{app.username}?start=info_{videoid}"
                thumbnail = None
                try:
                    if youtube.use_fallback:
                        file_path, _data, video = await fallback.download(
                            title[:12],
                            video=video,
                        )
                        direct = None
                        title = _data.get("title", title)
                        thumbnail = _data.get("thumb")
                        flink = _data.get("url", flink)
                        check[0]["dur"] = _data.get("duration_min", check[0]["dur"])
                    else:
                        try:
                            file_path, direct = await youtube.download(
                                videoid,
                                mystic,
                                videoid=True,
                                video=video,
                            )
                        except Exception:
                            youtube.use_fallback = True
                            file_path, _data, video = await fallback.download(
                                title[:12],
                                video=(True if str(streamtype) == "video" else False),
                            )
                            title = _data.get("title", title)
                            thumbnail = _data.get("thumb")
                            flink = _data.get("url", flink)
                            check[0]["dur"] = _data.get("duration_min", check[0]["dur"])
                except Exception:
                    return await mystic.edit_text(
                        _["call_7"], disable_web_page_preview=True
                    )

                if video:
                    stream = MediaStream(
                        file_path,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    try:
                        image = await youtube.thumbnail(videoid, True)
                    except Exception:
                        image = None
                    if image and config.PRIVATE_BOT_MODE:
                        stream = MediaStream(
                            image,
                            audio_path=file_path,
                            audio_parameters=audio_stream_quality,
                            video_parameters=video_stream_quality,
                        )
                    else:
                        stream = MediaStream(
                            file_path,
                            audio_parameters=audio_stream_quality,
                            video_flags=MediaStream.Flags.IGNORE,
                        )
                try:
                    await client.play(chat_id, stream, config=call_config)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
                    )
                img = await gen_thumb(videoid, thumbnail)
                button = stream_markup(_, videoid, chat_id)
                await mystic.delete()
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        flink,
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            elif "index_" in queued:
                stream = (
                    MediaStream(
                        videoid,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                    if str(streamtype) == "video"
                    else MediaStream(
                        videoid,
                        audio_parameters=audio_stream_quality,
                        video_flags=MediaStream.Flags.IGNORE,
                    )
                )
                try:
                    await client.play(chat_id, stream, config=call_config)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
                    )
                button = telegram_markup(_, chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=config.STREAM_IMG_URL,
                    caption=_["stream_2"].format(user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                url = check[0].get("url")
                if videoid == "telegram":
                    image = None
                elif videoid == "soundcloud":
                    image = None

                elif "saavn" in videoid:
                    url = check[0].get("url")
                    details = await saavn.info(url)
                    image = details["thumb"]
                else:
                    try:
                        image = await youtube.thumbnail(videoid, True)
                    except Exception:
                        image = None
                if video:
                    stream = MediaStream(
                        queued,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    if image and config.PRIVATE_BOT_MODE:
                        stream = MediaStream(
                            image,
                            audio_path=queued,
                            audio_parameters=audio_stream_quality,
                            video_parameters=video_stream_quality,
                        )
                    else:
                        stream = MediaStream(
                            queued,
                            audio_parameters=audio_stream_quality,
                            video_flags=MediaStream.Flags.IGNORE,
                        )
                try:
                    await client.play(chat_id, stream, config=call_config)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
                    )
                if videoid == "telegram":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=(
                            config.TELEGRAM_AUDIO_URL
                            if str(streamtype) == "audio"
                            else config.TELEGRAM_VIDEO_URL
                        ),
                        caption=_["stream_1"].format(
                            title, config.SUPPORT_GROUP, check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                elif videoid == "soundcloud":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=config.SOUNCLOUD_IMG_URL,
                        caption=_["stream_1"].format(
                            title, config.SUPPORT_GROUP, check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                elif "saavn" in videoid:
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=image,
                        caption=_["stream_1"].format(title, url, check[0]["dur"], user),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"

                else:
                    img = await gen_thumb(videoid)
                    button = stream_markup(_, videoid, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=img,
                        caption=_["stream_1"].format(
                            title[:27],
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        pings = []
        for call in self.calls:
            pings.append(call.ping)
        if pings:
            return str(round(sum(pings) / len(pings), 3))
        else:
            logger.error("No active clients for ping calculation.")
            return "No active clients"

    async def start(self):
        """Starts all PyTgCalls instances for the existing userbot clients."""
        logger.info("Starting PyTgCall Clients")
        await asyncio.gather(*[c.start() for c in self.calls])

    async def stop(self):
        t = []
        for x in await get_active_chats():
            t.append(self.leave_call(x))
        await asyncio.gather(*t, return_exceptions=True)

    async def decorators(self):
        for call in self.calls:

            @call.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
            async def stream_services_handler(client, update: ChatUpdate):
                await self.stop_stream(update.chat_id)

            @call.on_update(filters.stream_end())
            async def stream_end_handler(client, update: StreamEnded):
                if not update.stream_type == StreamEnded.Type.AUDIO:
                    return
                await self.change_stream(client, update.chat_id)

    def __getattr__(self, name):
        if not self.calls:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )
        first_call = self.calls[0]
        if hasattr(first_call, name):
            return getattr(first_call, name)
        raise AttributeError(
            f"'{type(first_call).__name__}' object has no attribute '{name}'"
        )


Yukki = Call()
