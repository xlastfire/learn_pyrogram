import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from helpers.penpals_values import COUNTRIES, GENDERS, AGES, AGES_SHOW
from helpers.logger import add_to_log
from pyrogram.errors import FloodWait
import re

url = 'https://www.penpalsnow.com/do/search.html'



def getIDs(text):
    ids = []
    for word in text:
        if 'id="' in word:
            ids.append(word.split('"')[1])
    return ids


def deEmojify(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


async def multipages(target=10, found=0, session=None, gender='female', age_group='19-22', country='UK', num=0,bot=None,update=None):
    if session is None:
        with requests.Session() as session:
            login_data = {
                'sex': gender,
                'agegroup': age_group,
                'hobbies': '',
                'country': country,
                'city': '',
                'language': '',
                'search': 'Find+penpals!%21',
                'numb': num,
                'search': 'Find+penpals!%21'
            }

            r = session.get(url)

            r = session.post(url, data=login_data)

    else:
        login_data = {
            'transfer': gender + '||X||' + age_group + '||X||' + country + '||X||||X||||X||||X||||X||',
            'numb': num,
            'search': 'Next 5 pen pal ads'
        }
        r = session.post(url, data=login_data)

    soup = BeautifulSoup(r.content, 'html5lib')

    uu = 'https://www.penpalsnow.com/_api/showemail.php?e='

    ids = getIDs(r.text.split(" "))

    paragraphs = soup.find_all('p')

    paras = []
    for para in paragraphs:
        paras.append(para)

    index = 0

    for i in range(2, len(paras)):
        vals = paras[i].find_all('span', class_='ppadvaluebold')
        if len(vals) != 3:
            continue
        # print(paras[i])
        name = str(vals[0].text).strip()
        gender = str(vals[1].text).strip()
        age = str(vals[2].text).strip()
        address = str(paras[i].find('address').find('span', class_='ppadvalue').text).strip().replace("\n",
                                                                                                      ',').replace(
            '       ', ' ')
        email = requests.get(uu + ids[index]).text

        para = str(paras[i].find('span', class_='ppadvaluemsg').text).strip().replace("\n\n", '\n')
        date = str(paras[i].find('span', class_='ppaddatevalue').text).strip()
        date1 = date[:4] + '/' + date[4:6] + '/' + date[6:]

        result = f'Name - {name} Age - {age} Gender - {gender} \nEmail - {email} Address - {address} \nLast Modified - {date1} \nMsg - {para[:900]}\n'

        try: 
            await bot.send_message(
                chat_id = update.chat.id,
                text = result
            )
        except FloodWait as e:
            sleep(e.x)
            await bot.send_message(
                chat_id = update.chat.id,
                text = result
            )
        found += 1
        index += 1

    if found >= target:
        return
    else:
        interval = randint(2, 5)
        await bot.send_message(
            chat_id = update.chat.id,
            text = f'\n>> Waiting - {interval}s for next <<'
        )
        sleep(interval)
        num += 5
        await multipages(target, found, session, gender, age_group, country, num, bot, update)

# await bot.send_message(
#             chat_id = update.chat.id,
#             reply_to_message_id = update.message_id,
#             text = "hi bn"
#     )

help_string = "Scraping PenpalsNow.com"
help_string += "\n<b>STRUCTURE ->  </b><code>penpals-t-g-a-c</code>"
help_string += "\nt - <b>target. should be positive number</b>"
help_string += "\ng - <b>gender. male or female. for both give me empty</b>"
help_string += "\na - <b>age_group. to see groups send me <code>penpals-ages</code> \n     for any give me empty</b>"
help_string += "\nc - <b>country. to see countries send me <code>penpals-countries</code> \n     for any give me empty</b>"
help_string += "\nAny Question - <b>Ask me @indexoutbound</b>"

async def print_countries(bot, update):
    small_list = []
    for country in COUNTRIES:
        if len(small_list) == 20:
            await bot.send_message(
            chat_id = update.chat.id,
            text = small_list
            )
            small_list = []
            continue
        small_list.append(country)
    if len(small_list) != 0:
        await bot.send_message(
            chat_id = update.chat.id,
            text = small_list
    )
    small_list = []
    return

async def print_ages(bot, update):
    await bot.send_message(
            chat_id = update.chat.id,
            text = AGES_SHOW
    )
    return

async def penpals_main(bot,update):

    text = update.text

    if '-' not in text:
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = help_string
        )
        return

    words = text.split('-')
    
    
    if text == 'penpals-t-g-a-c':
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = 'WTF! Give me values.\nCheck STRUCTURE -> <code>penpals-help</code>'
        )
        return
    if len(words) == 2 and words[1] == 'help':
        
        await bot.send_message(
            chat_id = update.chat.id,
            reply_to_message_id = update.message_id,
            text = help_string
        )
        return
    
    if len(words) == 2 and words[1] == 'countries':
        await print_countries(bot, update)
        return

    if len(words) == 2 and words[1] == 'ages':
        await print_ages(bot, update)
        return

    if len(words) == 5 :
        target = words[1]
        gender = words[2].lower()
        age_group = words[3]
        country = words[4].lower()
        try:
            target = int(words[1])
            if target < 0 or target > 25:
                await bot.send_message(
                    chat_id = update.chat.id,
                    reply_to_message_id = update.message_id,
                    text = "Send between 0-25 not to be blocked. Selected to 10"
                )
                target = 10
        except:
            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = "Invalid Target Input!. Selected to 5"
            )
            target = 5
        if gender not in GENDERS:
            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = "Cannot find Gender. So selected any mode"
            )
            gender =''
        if age_group not in AGES:
            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = "Cannot find age_group. So selected any mode.\nTo know age groups send me \n<code>penpals-ages</code>"
            )
            age_group = ''
        if country not in COUNTRIES:
            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = "Cannot find country. So selected any mode.\nTo know age groups send me \n<code>penpals-countries</code>"
            )
            country = ''
        
        else:
            await bot.send_message(
                chat_id = update.chat.id,
                reply_to_message_id = update.message_id,
                text = help_string
            )
        
        await add_to_log(f'{update.chat.id} - penpalsnow t - {target} g - {gender} a - {age_group} c - {country}')
        await multipages(target, found=0, gender=gender, age_group=AGES[age_group], country=COUNTRIES[country.lower()], num=0,bot=bot,update=update)
