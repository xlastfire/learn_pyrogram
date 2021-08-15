import requests as req
from bs4 import BeautifulSoup as Soup
from time import sleep
from random import randint
from helpers.logger import add_to_log

URL = 'http://colombotimes.lk/'


async def colombotimes_main(bot, update):

    await add_to_log(f'{update.chat.id} - colombotimes_main')
    r = req.get(URL)
    soup = Soup(r.content, 'html5lib')

    container = soup.find('div',class_='loop-container')
    news = container.find_all('div')

    for each_news in news:
        try:
          news_text = each_news.find('article').text
        except:
          continue
        if news_text is None:
          continue
        try:
          news_link = each_news.a['href']
        except:
          continue
        result = f'Link - {news_link}'
        await bot.send_message(
            chat_id = update.chat.id,
            text = result
        )
        interval = randint(3,5)
        sleep(interval)
    await bot.send_message(
            chat_id = update.chat.id,
            text = 'Send me one of these links to get more details'
    )

async def colombotime_page(bot, update):
    url = update.text
    await add_to_log(f'{update.chat.id} - colombotimes_page - {url}')
    r = req.get(url)
    soup = Soup(r.content,'html5lib')
    news = soup.find_all('p')
    index = len(news)

    temp = ''
    for i in range(1,index-1):
        
        if len(temp) + len(news[i].text) < 1000:
              temp += '\n' + news[i].text
              continue
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
