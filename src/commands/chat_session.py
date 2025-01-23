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

# TODO (Gabe) Make this more generic and also create the chat session as well
async def create_chat_thread(ctx: discord.Interaction, prompt: str, model: str):
    if isinstance(ctx.channel, discord.Thread):
        await ctx.respond("You are already in a thread.")
        return

    thread = await ctx.channel.create_thread(
        name=f"[{ctx.author.display_name}] [Model={model}] - {prompt[:97] + "..." if len(prompt) > 100 else prompt}",
        type=discord.ChannelType.public_thread,
        auto_archive_duration=10080 # one week
    )

    # Create welcome message
    await ctx.respond(f"**{ctx.author.mention} | Model: {model} | <#{thread.id}>**")
    await thread.send(f"**Hello {ctx.author.mention}! I'm here to assist you. Please wait as I read your prompt.**\n\nPrompt: {prompt}")
    await thread.add_user(ctx.author)

    return thread

@chat_session.command()
async def gemini(ctx: discord.Interaction, prompt: str):
    thread = await create_chat_thread(ctx, prompt, "gemini-1.5-flash")

    session = {
        "id": thread.id,
        "summary_chat": "",
        "model": "GEMINI_NORMAL", 
        "chat": [{
            "role": "user",
            "msg": prompt
        }]
    }

    redis_store.set(thread.id, json.dumps(session))
    await send_message(thread.id, prompt)


@chat_session.command()
async def gpt(ctx: discord.Interaction, prompt: str):
    thread = await create_chat_thread(ctx, prompt, "gpt-4o-mini")

    session = {
        "id": thread.id,
        "summary_chat": "",
        "model": "GPT_NORMAL", 
        "chat": [{
            "role": "user",
            "msg": prompt
        }]
    }

    redis_store.set(thread.id, json.dumps(session))
    await send_message(thread.id, prompt)


@chat_session.command()
async def o1mini(ctx: discord.Interaction, prompt: str):
    thread = await create_chat_thread(ctx, prompt, "o1-mini")

    session = {
        "id": thread.id,
        "summary_chat": "",
        "model": "O1MINI_NORMAL", 
        "chat": [{
            "role": "user",
            "msg": prompt
        }]
    }

    redis_store.set(thread.id, json.dumps(session))
    await send_message(thread.id, prompt)
