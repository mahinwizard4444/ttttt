from pyrogram import Client, filters
from pyrogram.types import Message
from requests import get
import os
import requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

caption = """
**✅ Logo Generated Successfully
Made With ❤ BY @BX_Botz**
    """
#logo creator
@Client.on_message(filters.command("logo"))
async def on_off_antiarab(_, message: Message):
    text = message.text.split(None, 1)[1]
    photo = get(f"https://single-developers.herokuapp.com/logo?name={text}").history[1].url
    await Client.send_photo(chat_id=message.chat.id, photo=photo, caption =caption.format(message.from_user.mention),
                 reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🖇 Telegraph Link 🖇", url=f"{photo}"
                    )
                ]
            ]
          ),
    )

#hq logo creator
@Client.on_message(filters.command("logohq"))
async def on_off_antiarab(_, message: Message):
    text = message.text.split(None, 1)[1]
    photo = get(f"https://api.single-developers.software/logohq?name={text}").history[1].url
    await Client.send_photo(chat_id=message.chat.id, photo=photo, caption =caption.format(message.from_user.mention),
                 reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "••Telegraph Link••", url=f"{photo}"
                    )
                ]
            ]
          ),
    )

#handwrite
@Client.on_message(filters.command("write"))
async def on_off_antiarab(_, message: Message):
    text = message.text.split(None, 1)[1]
    API = "https://api.single-developers.software/write"
    body = {     
     "text":f"{text}"     
    }
    req = requests.post(API, headers={'Content-Type': 'application/json'}, json=body)
    img = req.history[1].url
    await Client.send_photo(chat_id=message.chat.id, photo=img, caption =caption.format(message.from_user.mention),
                 reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "••Telegraph Link••", url=f"{img}"
                    )
                ]
            ]
          ),
    )
