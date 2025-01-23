import os
from dotenv import load_dotenv
load_dotenv() 

from src.bot import bot

bot.run(os.getenv("DISCORD_BOT_TOKEN"))