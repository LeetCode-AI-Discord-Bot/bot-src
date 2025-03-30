import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv() 

class Funny(commands.Cog, name="funny"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="funny", description="Send a random funny gif")
    @app_commands.guilds(discord.Object(id=os.getenv("SERVER_ID")))
    async def funny(self, ctx):
        await ctx.send("https://tenor.com/view/leaves-gif-19732729")

async def setup(bot) -> None:
    await bot.add_cog(Funny(bot))