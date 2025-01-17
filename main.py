import os
from dotenv import load_dotenv
load_dotenv() 

from src.client import bot

bot.run(os.getenv("DISCORD_BOT_TOKEN"))