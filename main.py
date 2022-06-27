import os
from dotenv import load_dotenv

load_dotenv()
print("e")
from discord_bot import bot

bot.run(os.getenv("BOT_TOKEN"))
