import pyrogram

from helpers.penpalsnow import penpals_main
from helpers.rata import rata_main, rata_page
from helpers.colombotimes import colombotime_page, colombotimes_main
from helpers.lankacnews import lankacnews_main, lankacnews_page
from helpers.xham import xham_main
from helpers.xvid import xvid_page_videos, xvid_search
from time import sleep

AUTHORIZED = []

async def is_sudo(bot,update):
    id = update.chat.id
    if int(id) == 844127137:
        return True
    return False

async def fill_auth():
    f = open('autho.txt','r')
    for line in f:
        AUTHORIZED.append(line.strip())
    f.close()

async def add_user(id,bot,update):
    
    if is_sudo(bot,update):
        with open('autho.txt','a') as f:
            f.write('\n' + id.strip())
        f.close()
        
        AUTHORIZED.append(id)
        

        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = "Successfully Added!"
        )
    else:
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = "You're not Sudo!"
        )

async def send_log(bot, update):
    if is_sudo(bot, update):
        await bot.send_document(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            document = 'helpers/log.txt'
        )
    else:
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = "You're not Sudo!"
        )

async def send_users(bot,update):
    await bot.send_message(
        chat_id = update.chat.id,
        reply_to_message_id = update.message_id,
        text = AUTHORIZED
    )
    # await bot.send_document(
    #     chat_id = update.chat.id,
    #     reply_to_message_id = update.message_id,
    #     document = 'autho.txt'
    # )


HELP = '''<code>help</code> -> <b>for this help menu</b>\n
<code>penpals-help</code> <b> -> for penpals scrape hints</b>\n
<code>rata.lk</code> <b> -> Today Latest 10 News from rata.lk</b>\n
<code>lankacnews</code> <b> -> Today Latest 10 News from lankacnews.lk</b>\n
<code>colombotimes</code> <b> -> Today Latest 10 News from colombotimes.lk</b>\n
<code>xhams-help</code> <b> -> Scrape Xhamster Search Page</b>\n
<code>xvid-help</code> <b> -> Generate Xvidoes Search Page Links</b>\n
<code>about <b> -> About</b></code>
<b>Any Question or Adding features\n->>> @indexoutbound <<<-/b>'''

ABOUT_TEXT = """
- **Bot :** `Simple Scraper`
- **Creator :** @indexoutbound
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram v1.2.0](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
"""
#- **Source :** [Click here](https://github.com/FayasNoushad/URL-Uploader)

# For checking file sending.
async def send(bot,update):

    await bot.send_photo(
        chat_id = update.chat.id,
        reply_to_message_id = update.message_id,
        photo = '11.jpg',
        caption = 'CapTest'
    )
    await bot.send_document(
        chat_id = update.chat.id,
        reply_to_message_id = update.message_id,
        document = 'sample.txt',
        caption = 'CapTest'
    )

@pyrogram.Client.on_message()
async def echo(bot, update):

    text = update.text.lower()

    if len(AUTHORIZED) == 0:
        await fill_auth()
        
    if str(update.chat.id) not in AUTHORIZED:
        await update.reply_text("You are Not authorized ask from - @indexoutbound")
        return

    if text == 'logs':
        await send_log(bot,update)
        return
    
    if text == 'xhams':
        await xham_main(bot,update)
        return

    if text == 'users':
        await send_users(bot,update)
        return

    if text.startswith('add'):
        words = text.split(' ')
        await add_user(words[1],bot,update)
        return

    if text == 'send':
        await send(bot,update)
        return

    if text == 'news':
        await colombotimes_main(bot,update)
        sleep(10)
        await rata_main(bot=bot, update=update)
        return

    if text == 'colombotimes':
        await colombotimes_main(bot,update)
        return

    if text == 'lankacnews':
        await lankacnews_main(bot, update)
        return

    if 'https://lankacnews.com/' in text:
        await lankacnews_page(bot,update)
        return

    if 'http://colombotimes.lk/' in text:
        await colombotime_page(bot,update)
        return

    if 'https://si.rata.lk/' in text:
        await rata_page(bot, update)
        return

    if text == 'rata.lk':
        await rata_main(bot=bot, update=update)
        return

    if text.startswith('penpals'):
        await penpals_main(bot, update)
        return

    if text == 'about':
        await update.reply_text(ABOUT_TEXT)
        return

    if text == 'help':
        await update.reply_text(HELP)
        return

    if 'xvideos.com/video' in text:
        await xvid_page_videos(bot,update)
        return
    
    if 'xsearch' in text:
        await xvid_search(bot,update)
        return