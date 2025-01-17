import os
from dotenv import load_dotenv
load_dotenv()

import discord

chat_session = discord.SlashCommandGroup(
    "chat-session", 
    "Create a new AI chat session", 
    guild_ids=[int(os.getenv("DISCORD_GUILD_ID"))],
    guild_only=True)

@chat_session.command()
async def google(ctx, prompt: str):
    thread = await ctx.channel.create_thread(
            name=f"[{ctx.author.display_name}] - {prompt[:17] + "..." if len(prompt) > 20 else prompt}",
            invitable=False,  # Set to True if you want others to join
        )
        
    # Send a welcome message in the thread
    await thread.send(f"**Hello {ctx.author.mention}! I'm here to assist you. Please wait as I read your prompt.**\nPrompt: {prompt}")
    await thread.add_user(ctx.author)

    await ctx.respond(f"**{ctx.author.mention} | Chat has been created: <#{thread.id}>**")

