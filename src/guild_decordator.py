import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv() 

# NOTE: Taken from chatgpt
def guild_decorator():
    if os.getenv("IS_PRODUCTION") == "True":
        return lambda x: x  # Don't restrict to a guild
    else:
        return app_commands.guilds(discord.Object(id=os.getenv("DISCORD_GUILD_ID"),))