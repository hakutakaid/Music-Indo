from typing import Union

from pyrogram.types import InlineKeyboardButton

from config import SUPPORT_CHANNEL, SUPPORT_GROUP, OWNER_ID
from MusicIndo import app


def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            ),
            InlineKeyboardButton(text=_["S_B_2"], callback_data="settings_helper"),
        ],
    ]
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}"),
                InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
            ]
        )
    else:
        if SUPPORT_CHANNEL:
            buttons.append(
                [InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}")]
            )
        if SUPPORT_GROUP:
            buttons.append(
                [InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}")]
            )
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text="Support", url=f"{SUPPORT_CHANNEL}"),
            InlineKeyboardButton(text="Add Me", url=f"https://t.me/{app.username}?startgroup=true"),
            InlineKeyboardButton(text="Owner", url=f"https://t.me/Usern4meDoestExist404"),
        ],
        [
            InlineKeyboardButton(text=_["S_B_8"], callback_data="settings_back_helper"),
        ],
        [
            InlineKeyboardButton(text="close", callback_data=f"close"),
        ]
    ]
    return buttons

def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="Add Me", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
        ],
    ]
    return buttons
