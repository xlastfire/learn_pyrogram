import requests
from bs4 import BeautifulSoup
from pyrogram.errors import FloodWait
from time import sleep
from helpers.logger import add_to_log

url = 'https://xhamster.com/search/'

help_string = "Scraping Xhamster.com"
help_string += "\n<b>STRUCTURE 1 -> </b><code>xham-s-p</code>"
help_string += "\n<b>STRUCTURE 2 -> </b><code>xham-s-p-m</code>"
help_string += "\ns - <b>search keyword.</b>"
help_string += "\np - <b>pages.should be below 20.</b>"
help_string += "\nm - <b>for mirror bot number(ex. /watch1).</b>"
help_string += "\nAny Question - <b>Ask me @indexoutbound</b>"


async def scrape(bot, update, search, page_count, mirror):

    temp_url = url + search
    pages = []
    pages.append(temp_url)
    for page_idx in range(2, page_count+1):
        pages.append(temp_url + "?page=" + str(page_idx))

    for page in pages:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html5lib')
        vid_links = soup.find_all('div', class_='video-thumb-info')
        for each_link in vid_links:
            if mirror != '':
                each_link = '/watch' + mirror + ' ' + each_link
            try:
                await bot.send_message(
                    chat_id = update.chat.id,
                    reply_to_message_id = update.message_id,
                    text = each_link
                )
            except FloodWait as e:
                sleep(e.x)
                await bot.send_message(
                    chat_id = update.chat.id,
                    reply_to_message_id = update.message_id,
                    text = each_link
                )
    return
        


async def xham_main(bot, update):
    text = update.text

    if '-' not in text:
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = help_string
        )
        return
    
    words = text.split('-')
    
    if len(words) == 2 and words[1].lower() == 'help':
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = help_string
        )
        return
    
    if len(words) != 3 and len(words) != 4:
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = help_string
        )
        return
    
    try:
        page_count = int(words[2])
        if page_count <= 0 or page_count > 20:
            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = '<b>Only allowed 1-20 pages.</b>'
            )
            return
    except:
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = "<b>Something error at page count!</b>"
        )
        return
    search_word = words[1].replace(' ','+')

    mirror = ''
    if len(words) == 4:
        mirror = words[3]

    await add_to_log(f'{update.chat.id} - xham - {search_word} - {page_count}')
    await scrape(bot,update,search_word,page_count,mirror)
    return