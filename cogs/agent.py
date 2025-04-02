import os
import discord
from discord.ext import commands
from discord import app_commands 
from dotenv import load_dotenv

load_dotenv() 

from src.react_agent import ReActAgent
from src.leetcode_problem import extract_problem_name
from src.redis_thread_storage import RedisThreadStorage

thread_storage = RedisThreadStorage()

class Agent(commands.Cog, name="Agent"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="session", description="Start a session with the LeetCode-Carti")
    @app_commands.guilds(discord.Object(id=os.getenv("SERVER_ID")))
    async def create_session(self, ctx, leetcode_url: str):
        message_sent = await ctx.send("Thread is being cooked for: " + leetcode_url)
        thread = None
        try:
            thread = await message_sent.create_thread(name=f"[LeanCodeCarti-Help] {extract_problem_name(leetcode_url)}", auto_archive_duration=10080)
            thread_storage.add(str(thread.id), str(ctx.author.id), leetcode_url)

            agent = ReActAgent(leetcode_url, str(thread.id))
            welcome_message = agent.process_message("Write a hello welcome message for me regarding the problem")
            await thread.send(welcome_message)

        except Exception as e:
            print(e)
            if thread is not None:
                thread_storage.delete(str(thread.id))
                await thread.delete()

            await message_sent.edit(content="Thread dead bro... SEND THE RIGHT URL NEXT TIME")
            return

        await message_sent.edit(content="Done eat up: " + leetcode_url)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        thread = thread_storage.get(str(message.channel.id))
        if (thread is not None and message.author.id != self.bot.user.id):
            try:
                agent = ReActAgent(thread.leetcode_url, str(message.channel.id))
                welcome_message = agent.process_message(message.content)
                await message.channel.send(welcome_message)
            except Exception as e:
                print(e)
                await message.channel.send("BRUH I'M DEAD...")

async def setup(bot) -> None:
    await bot.add_cog(Agent(bot))