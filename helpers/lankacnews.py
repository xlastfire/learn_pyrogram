import requests as req
from bs4 import BeautifulSoup as Soup
from pyrogram.errors import FloodWait
from time import sleep
from helpers.logger import add_to_log

URL = 'https://lankacnews.com/news/'

async def lankacnews_page(bot,update):
    url = update.text
    await add_to_log(f'{update.chat.id} - lankacnews_page - {url}')
    r = req.get(url)
    soup = Soup(r.content,'html5lib')
    news = soup.find('article',class_='col-lg-12 col-md-12 news-item main-news main-news-item')
    paras = news.find_all('p')
    temp = ''
    for para in paras:
        para_text = para.text

        if len(temp) + len(para_text) < 1000:
            temp += '\n' + para_text
            continue
        try:
            await bot.send_message(
                    chat_id = update.chat.id,
                    text = temp
            )
        except FloodWait as e:
            sleep(e.x)
            await bot.send_message(
                chat_id = update.chat.id,
                text = temp
            )
        temp = ''
    if temp != '':
        await bot.send_message(
                chat_id = update.chat.id,
                text = temp
        )

async def lankacnews_main(bot, update):

    await add_to_log(f'{update.chat.id} - lankacnews_page')
    r = req.get(URL)
    soup = Soup(r.content,'html5lib')

    news = soup.find_all('article',class_='col-lg-6 col-md-12 news-item main-news main-news-item cat-view-news-item clearfix')

    for each_news in news:
        
        news_link = each_news.a['href']
        
        try:

            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = news_link
            )
        except FloodWait as e:
            sleep(e.x)
            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = news_link
            )
    await bot.send_message(
            chat_id = update.chat.id,
            text = 'Send me one of these links to get more details'
    )
        