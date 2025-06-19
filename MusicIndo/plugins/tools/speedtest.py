#
#
import asyncio

import speedtest

from strings import command
from MusicIndo import app
from MusicIndo.misc import SUDOERS


async def testspeed(m):
    try:
        test = await asyncio.to_thread(speedtest.Speedtest)
        await asyncio.to_thread(test.get_best_server)

        m = await m.edit("⇆ Running Download Speedtest ...")
        await asyncio.to_thread(test.download)

        m = await m.edit("⇆ Running Upload SpeedTest...")
        await asyncio.to_thread(test.upload)

        await asyncio.to_thread(test.results.share)
        result = await asyncio.to_thread(test.results.dict)

        m = await m.edit("↻ Sharing SpeedTest results")
    except Exception as e:
        return await m.edit(str(e))

    return result


@app.on_message(command("SPEEDTEST_COMMAND") & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("ʀᴜɴɴɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ")
    result = await testspeed(m)
    output = f"""**Speedtest Results**
    
<u>**Client:**</u>
**ISP :** {result["client"]["isp"]}
**Country :** {result["client"]["country"]}
  
<u>**Server:**</u>
**Name :** {result["server"]["name"]}
**Country:** {result["server"]["country"]}, {result["server"]["cc"]}
**Sponsor:** {result["server"]["sponsor"]}
**Latency:** {result["server"]["latency"]}  
**Ping :** {result["ping"]}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
