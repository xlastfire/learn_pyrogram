import requests
from bs4 import BeautifulSoup
from pyrogram.errors import FloodWait
from helpers.logger import add_to_log
from time import sleep


XVID_SEARCH_HELP = '''<b>Get Search Results Page Links</b>\n
<code>xsearch-uk teen-10</code> <b> -> Command</b>\n
Here - <b>uk teen</b> <b> -> Search Keyword</b>
     - <b>10</b> <b> -> Number of pages</b>
'''    
async def xvid_search(bot,update):
    
    text = update.text
    
    if '-' not in text:
        await update.reply_text(XVID_SEARCH_HELP)
        return

    words = text.split('-')
    
    if words[1] == 'help' or len(words) != 3:
        await update.reply_text(XVID_SEARCH_HELP)
        return
        
    key = words[1]
    try:
        pages = int(words[2])
    except:
        await update.reply_text(f'"{words[2]}" should be a number')
        return
    await add_to_log(f'{update.chat.id} - xvid_search - {key} - {pages}')
    SEARCH_URL = 'https://www.xvideos.com/?k=' + key.replace(' ','+')

    for page in range(1,pages):
        try:
            await bot.send_message(
                chat_id = update.chat.id,
                text = SEARCH_URL + '&p=' + str(page)
            )
        except FloodWait as e:
            sleep(e.x)
            await bot.send_message(
                chat_id = update.chat.id,
                text = SEARCH_URL + '&p=' + str(page)
            )
    return

async def xvid_page_videos(bot,update):
    text = update.text
    PREFIX = '/watch1 https://www.xvideos.com'
    url = text.strip()
    await add_to_log(f'{update.chat.id} - xvid_page_videos - {url}')
    req = requests.get(url)
    words = req.text.split(' ')
    links = []
    for word in words:
        if 'i-like' in word:
            continue
        if 'href="/video' in word and '><' not in word:
            link = word.split('"')[1]
            links.append(PREFIX + link)
    words = []

    for link in links:
        try:        
            await bot.send_message(
                chat_id = update.chat.id,
                text = link
            )
        except FloodWait as e:
            sleep(e.x)
            await bot.send_message(
                chat_id = update.chat.id,
                text = link
            )


