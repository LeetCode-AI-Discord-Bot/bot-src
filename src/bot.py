import discord

from src.redis_store import redis_store
from src.commands.chat_session import chat_session
from src.llm.chat_manager import send_message

# Setup the bot
_intents = discord.Intents.default()
_intents.message_content = True  # Allow reading message content
_intents.guilds = True
_intents.members = True  # Needed for member-related events

bot = discord.Bot(intents=_intents)

# TODO (Gabe) Setup a logger for bot
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


# TODO (Gabe) Remove this later as it doesn't work (still don't know why) and 
#   use redis expiration for this. Maybe set up a cron job?
@bot.event
async def on_thread_remove(thread: discord.Thread):
    # Check if the archived status has changed
    redis_store.delete(thread.id)
    await thread.send("**Thread has been archived.** | Please create a new thread if you wish to continue using the bot.")
    await thread.archive(locked=True)
    print(f"The thread '{thread.name}' is now archived.")


@bot.event
async def on_message(message: discord.Message):
    if not message.author.bot and isinstance(message.channel, discord.Thread):
        message.channel.archived = True
        await send_message(message.channel.id, message.content)

bot.add_application_command(chat_session)
