import os
import json
import discord
from dotenv import load_dotenv
load_dotenv()

from src.llm.chat_manager import send_message
from src.redis_store import redis_store

chat_session = discord.SlashCommandGroup(
    "chat-session", 
    "Create a new AI chat session", 
    guild_ids=[int(os.getenv("DISCORD_GUILD_ID"))])

@chat_session.command()
async def google(ctx, prompt: str):
    if isinstance(ctx.channel, discord.Thread):
        await ctx.respond("You are already in a thread.")
        return

    thread = await ctx.channel.create_thread(
        name=f"[{ctx.author.display_name}] - {prompt[:97] + "..." if len(prompt) > 100 else prompt}",
        type=discord.ChannelType.public_thread,
        auto_archive_duration=10080 # one week
    )

    await ctx.respond(f"**{ctx.author.mention} | Model: Google | Chat has been created: <#{thread.id}>**")
    # Send a welcome message in the thread
    await thread.send(f"**Hello {ctx.author.mention}! I'm here to assist you. Please wait as I read your prompt.**\nPrompt: {prompt}")
    await thread.add_user(ctx.author)

    session = {
        "id": thread.id,
        "summary_chat": "",
        "model": "GOOGLE_NORMAL", 
        "chat": [{
            "role": "user",
            "msg": prompt
        }]
    }

    redis_store.set(thread.id, json.dumps(session))
    await send_message(thread.id, prompt)

