import os
import logging


# Creating and configuring handler
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[%(asctime)s : %(levelname)s] - %(message)s",
        datefmt='%H:%M:%S'
    )
)

# Creating and configuring logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Telegram token
TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN')

# Openai token
OPENAI_TOKEN: str = os.getenv('OPENAI_TOKEN')

# Bot name (be careful)
# The bot answers only if the message starts with its name
BOT_NAME: str = os.getenv('BOT_NAME')

# Openai ! chat ! model
# using gpt-3.5-turbo recommended
AI_MODEL: str = os.getenv('AI_MODEL')

# It's required
INSTRUCTIONS: str = os.getenv('INSTRUCTIONS')
