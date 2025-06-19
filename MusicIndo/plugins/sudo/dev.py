#
#

# This aeval and sh module is taken from < https://github.com/TheHamkerCat/WilliamButcherBot >
# Credit goes to TheHamkerCat.
#

import asyncio
import contextlib
import os
import traceback
from io import StringIO
from time import time

import aiofiles
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MusicIndo import app
from MusicIndo.misc import SUDOERS


async def aexec(code, client, message):
    local_vars = {
        "__builtins__": __builtins__,  # DON'T REMOVE THIS
        "app": app,
    }
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n")),
        local_vars,
    )
    __aexec_func = local_vars["__aexec"]
    return await __aexec_func(client, message)


@app.on_edited_message(
    filters.command(["ev", "eval"]) & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
@app.on_message(
    filters.command(["ev", "eval"]) & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await message.reply(text="<b>Give me something to exceute</b>")
    try:
        cmd = message.text.markdown.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    redirected_output = redirected_error = StringIO()
    stdout, stderr, exc = None, None, None
    with (
        contextlib.redirect_stdout(redirected_output),
        contextlib.redirect_stderr(redirected_error),
    ):
        try:
            await aexec(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>RESULTS:</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        async with aiofiles.open(filename, "w+", encoding="utf8") as out_file:
            await out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2 - t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>EVAL :</b>\n<code>{cmd[0:980]}</code>\n\n<b>Results:</b>\nAttached Document",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2 - t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await message.reply(text=final_output, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, query):
    callback_data = query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if query.from_user.id != int(user_id):
        try:
            return await query.answer(
                "This is not for you stay away from here", show_alert=True
            )
        except Exception:
            return
    await query.message.delete()
    try:
        await query.answer()
    except Exception:
        return


@app.on_edited_message(
    filters.command("sh") & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
@app.on_message(filters.command("sh") & SUDOERS & ~filters.forwarded & ~filters.via_bot)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("<b>Give some commands like:</b>\n/sh git pull")

    text = message.text.markdown.split(None, 1)[1]
    output = ""

    async def run_command(command):
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            return stdout.decode().strip(), stderr.decode().strip()
        except Exception:
            return None, traceback.format_exc()

    if "\n" in text:
        commands = text.split("\n")
        for cmd in commands:
            stdout, stderr = await run_command(cmd)
            output += f"<b>Command:</b> {cmd}\n"
            if stdout:
                output += f"<b>Output:</b>\n<pre>{stdout}</pre>\n"
            if stderr:
                output += f"<b>Error:</b>\n<pre>{stderr}</pre>\n"
    else:
        stdout, stderr = await run_command(text)
        if stdout:
            output += f"<b>Output:</b>\n<pre>{stdout}</pre>\n"
        if stderr:
            output += f"<b>Error:</b>\n<pre>{stderr}</pre>\n"

    if not output.strip():
        output = "<b>OUTPUT :</b>\n<code>None</code>"

    if len(output) > 4096:
        async with aiofiles.open("output.txt", "w+") as file:
            await file.write(output)
        await app.send_document(
            message.chat.id,
            "output.txt",
            reply_to_message_id=message.id,
            caption="<code>Output</code>",
        )
        os.remove("output.txt")
    else:
        await message.reply(text=output)

    await message.stop_propagation()
