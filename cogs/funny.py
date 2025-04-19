import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
from src.guild_decordator import guild_decorator 

class Funny(commands.Cog, name="funny"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="crashout-cashout", description="BURH I'M FINNA CRASH OUT ON THIS")
    @guild_decorator()
    async def ye_cashout_music(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=XsO9ZsJuamY")

    @commands.hybrid_command(name="goodcredit", description="CARTI MY EVIL TWIN! CARTI MY EVIL TWIN! CARTI MY EVIL TWIN! CARTI MY EVIL TWIN!")
    @guild_decorator()  
    async def carti_evil_jorden_music(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=58JU9solXFw")

    @commands.hybrid_command(name="lean-drop", description="I NEED IT!!!!!!!!!!!!!")
    @guild_decorator()
    async def fake_sponser(self, ctx):
        await ctx.send("# Use code: leencodecarti2020 for ur order!!!!\n https://gamersupps.gg/products/lean-100-servings?_pos=1&_sid=3460500c2&_ss=r")

    @commands.hybrid_command(name="ye-moment", description="THEY TOLD ME TO GET OFF OF TWITTER, LOL, NEVER!!!!!!!")
    @guild_decorator()
    async def ye_moment(self, ctx):
        await ctx.send("https://i.pinimg.com/originals/6e/5c/2f/6e5c2fd2e5f101c74f20a65f4fe9c396.gif")

    @commands.hybrid_command(name="best-tyler-song", description="TYLER!!!!!!")
    @guild_decorator()
    async def best_tyler_song(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=uLXPCPkQBh0")

async def setup(bot) -> None:
    await bot.add_cog(Funny(bot))