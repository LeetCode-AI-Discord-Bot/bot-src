import discord

from .commands.chat_session import chat_session

# Setup the bot
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
intents.guilds = True
intents.members = True  # Needed for member-related events

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


bot.add_application_command(chat_session)