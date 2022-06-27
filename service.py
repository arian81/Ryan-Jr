import daemon
from discord_bot import bot
import os
from dotenv import load_dotenv

load_dotenv()

with daemon.DaemonContext():
    bot.run(os.getenv("BOT_TOKEN"))
