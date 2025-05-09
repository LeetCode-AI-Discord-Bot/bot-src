import logging

import os

if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logger
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("./logs/bot.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

# Example usage
logger = logging.getLogger("BOT")
