import logging
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument
from database.ia_filterdb import get_search_results
from utils import is_subscribed, get_size
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME


@Client.on_inline_query()
async def answer(bot, query):
    """Show search results for given inline query"""

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='Join Updates Channel To Use This Bot 😌',
                           switch_pm_parameter="subscribe")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    files, next_offset, total = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)

    for file in files:
        title=file.file_name
        size=get_size(file.file_size)
        f_caption=file.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                print(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{file.file_name}"
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                file_id=file.file_id,
                caption=f_caption,
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results - {total}"
        if string:
            switch_pm_text += f" for {string}"
        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except QueryIdInvalid:
            pass
        except Exception as e:
            logging.exception(str(e))
            await query.answer(results=[], is_personal=True,
                           cache_time=cache_time,
                           switch_pm_text=str(e)[:63],
                           switch_pm_parameter="error")
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")


def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('🔍 Search Again', switch_inline_query_current_chat=query),
            InlineKeyboardButton('🧩 Other Bots', url='https://t.me/BX_Botz/31')
        ]
        ]
    return InlineKeyboardMarkup(buttons)


async def inlineX1(bot, update, searche):

          answers = []
          search_ts = searche
          query = search_ts.split(" ", 1)[-1]
          torrentList = await SearchYTS(query)
          if not torrentList:
              answers.append(InlineQueryResultArticle(title="No Torrents Found in ThePirateBay!",
              description=f"Can't find torrents for {query} in ThePirateBay !!",
              input_message_content=InputTextMessageContent(
              message_text=f"No Torrents Found For `{query}` in ThePirateBay !!", parse_mode="Markdown"),
              reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Try Again", switch_inline_query_current_chat="1 ") ] ] ) ) )
          else:
              for i in range(len(torrentList)):
                  dl_links = "- " + "\n\n- ".join(torrentList[i]['Downloads'] )
                  answers.append(InlineQueryResultArticle(title=f"name",
                  description=f"Language: English\nLikes: 5, Rating: none",
                  input_message_content=InputTextMessageContent(
                  message_text=f"**Genre:** a"
                               f"**Torrent Download Links:",
                               parse_mode="Markdown", disable_web_page_preview=True),
                  reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton("Search Again", switch_inline_query_current_chat="1 ") ] ] ),
                  thumb_url=torrentList[i]["Poster"] ) )
          try:
              await update.answer(results=answers, cache_time=0)
          except QueryIdInvalid:
              await asyncio.sleep(5)
          try:
              await update.answer(results=answers, cache_time=0,
              switch_pm_text="Error: Search timed out!",
              switch_pm_parameter="start",)
          except QueryIdInvalid:
              pass
