import requests as req
from bs4 import BeautifulSoup as Soup
from time import sleep
from random import randint
from pyrogram.errors import FloodWait
from helpers.logger import add_to_log

url = 'https://si.rata.lk/category/%e0%b6%b4%e0%b7%94%e0%b7%80%e0%b6%ad%e0%b7%8a/'

async def rata_main(bot,update):
    await add_to_log(f'{update.chat.id} - rata.lk_main')
    r = req.get(url)
    soup = Soup(r.content, 'html5lib')
    news = soup.find_all('div',class_='tdb_module_loop td_module_wrap td-animation-stack')

    for each_news in news:
        
        header = each_news.h3.text
        description = each_news.find('div',class_='td-excerpt').text
        link = each_news.find_all('a')[-1]['href']
        # msg = f'<b>{header}</b> \n {description} \n\n Link - {link}'
        msg = f'Link - {link}'

        try:
            mes = await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = msg
            )
        except FloodWait as e:
            sleep(e.x)
            mes = await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = msg
            )
        sleep(randint(4,8))
    
    await bot.send_message(
            chat_id = update.chat.id,
            text = 'Send me one of these links to get more details'
    )

async def rata_page(bot, update):
    
    url = update.text
    await add_to_log(f'{update.chat.id} - rata.lk_page - {url}')
    r = req.get(url)
    soup = Soup(r.content,'html5lib')
    paras_position = soup.find_all('div',class_='tdb-block-inner td-fix-index')[13]
    paragraphs = paras_position.find_all('p')

    temp = ''
    for para in paragraphs:
        if len(temp) + len(para.text) < 1000:
            temp += '\n' + para.text
            continue
        try:
            await bot.send_message(
                chat_id = update.chat.id,
                text = para.text
            )
        except FloodWait as e:
            sleep(e.x)
            await bot.send_message(
                chat_id = update.chat.id,
                text = para.text
            )
        temp = ''
    if temp != '':
        await bot.send_message(
                chat_id = update.chat.id,
                text = temp
        )