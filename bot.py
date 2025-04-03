import os
import discord
from discord.ext import commands
from src.logger import logger
from dotenv import load_dotenv

load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
intents.guilds = True
intents.members = True  # Needed for member-related events

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=intents, help_command=None, command_prefix="/")
        self.redis = None

    async def on_ready(self) -> None:
        logger.info(f"Main Server = {os.getenv("SERVER_ID")}")
        logger.info(f"Logged in as {self.user.name}#{self.user.discriminator}")
        logger.info(f"Running...")

    async def load_cogs(self) -> None:
        for filename in os.listdir("./cogs"):
            logger.info(f"Loading cog {filename[:-3]}")
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"Loaded cog {filename[:-3]}")
                except Exception as e:
                    logger.error(f"Failed to load cog {filename[:-3]}: {str(e)}")

    async def setup_hook(self) -> None:
        logger.info("Setting up bot...")
        await self.load_cogs()
        await self.tree.sync(guild=discord.Object(id=os.getenv("SERVER_ID")))

    async def on_message(self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)


bot = DiscordBot()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))