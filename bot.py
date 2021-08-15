import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config
    # from sample_config import Config


from pyrogram import idle
from pyrogram import Client

if __name__ == '__main__':

    plugins = dict(
        root = 'plugins'
    )

    app = Client(
        "MyBot",
        bot_token = Config.BOT_TOKEN,
        api_id = Config.APP_ID,
        api_hash = Config.API_HASH,
        plugins = plugins
    )
    
    app.run()
    idle()
