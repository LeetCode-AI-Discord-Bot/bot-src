from dotenv import load_dotenv
load_dotenv() 

import discord
import os

# Setup the bot
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
intents.members = True  # Needed for member-related events

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))