import toml
from environs import Env
from munch import DefaultMunch


__all__ = (
    'TELEGRAM_TOKEN',
    'TELEGRAM_OWNER_ID',
    'TELEGRAM_OWNER_USERNAME',
    'DATABASE_URI',
    'TELEGRAM_BOT_NAME',
    'OPENAI_SECRET_KEY',
    'OPENAI_PROJECT_ID',
    'OPENAI_TEXT_MODEL',
    'OPENAI_IMAGE_MODEL',
    'OPENAI_MODEL_INSTRUCTIONS',
    'app_config'
)


env = Env()
env.read_env()


# Telegram access token (from @BotFather)
TELEGRAM_TOKEN: str = env.str('TELEGRAM_TOKEN')
# Telegram admin id
TELEGRAM_OWNER_ID: int = env.int('TELEGRAM_OWNER_ID')
# Telegram owner username
TELEGRAM_OWNER_USERNAME: str = env.str('TELEGRAM_OWNER_USERNAME')
# Bot name
TELEGRAM_BOT_NAME: str = env.str('TELEGRAM_BOT_NAME')
# Database credentials
DATABASE_URI: str = env.str('DATABASE_URI')
# OpenAI API key
OPENAI_SECRET_KEY: str = env.str('OPENAI_SECRET_KEY')
# OpenAI Project ID
OPENAI_PROJECT_ID: str = env.str('OPENAI_PROJECT_ID')
# Default text-model to use
OPENAI_TEXT_MODEL: str = env.str('OPENAI_TEXT_MODEL')
# Default imagegen-model to use
OPENAI_IMAGE_MODEL: str = env.str('OPENAI_IMAGE_MODEL')
# `developer` instructions (define how to act)
OPENAI_MODEL_INSTRUCTIONS: str = env.str('OPENAI_MODEL_INSTRUCTIONS')

# Load app config (app_config.toml) file
with open('app_config.toml', 'r') as f:
    app_config = DefaultMunch.fromDict(toml.load(f))
