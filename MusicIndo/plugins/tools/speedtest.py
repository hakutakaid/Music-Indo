import asyncio

import speedtest
from pyrogram import filters
from MusicIndo.misc import SUDOERS
from strings import get_command
from MusicIndo import app

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆...")
        test.download()
        m = m.edit("⇆......")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("maksimal kecepatan server")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**mendapatkan kecepatan server**
    
<u>**ᴄʟɪᴇɴᴛ:**</u>
**ɪsᴘ :** {result['client']['isp']}
**ᴄᴏᴜɴᴛʀʏ :** {result['client']['country']}
  
<u>**sᴇʀᴠᴇʀ :**</u>
**ɴᴀᴍᴇ :** {result['server']['name']}
**ᴄᴏᴜɴᴛʀʏ :** {result['server']['country']}, {result['server']['cc']}
**sᴘᴏɴsᴏʀ :** {result['server']['sponsor']}
**ʟᴀᴛᴇɴᴄʏ :** {result['server']['latency']}  
**ᴘɪɴɢ :** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
