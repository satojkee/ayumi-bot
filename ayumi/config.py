"""This module loads application configuration."""


import tempfile
from dataclasses import dataclass

from toml import load
from environs import Env
from munch import DefaultMunch


__all__ = (
    'TELEGRAM_TOKEN',
    'TELEGRAM_OWNER_ID',
    'DATABASE_URI',
    'TELEGRAM_BOT_NAME',
    'OPENAI_SECRET_KEY',
    'OPENAI_PROJECT_ID',
    'TEMP_DIR',
    'app_config',
    'ChatTypes'
)


env = Env()
env.read_env()


# Telegram access token (from @BotFather)
TELEGRAM_TOKEN: str = env.str('TELEGRAM_TOKEN')
# Telegram admin id
TELEGRAM_OWNER_ID: int = env.int('TELEGRAM_OWNER_ID')
# Bot name
TELEGRAM_BOT_NAME: str = env.str('TELEGRAM_BOT_NAME')
# Database credentials
DATABASE_URI: str = env.str('DATABASE_URI')
# OpenAI API key
OPENAI_SECRET_KEY: str = env.str('OPENAI_SECRET_KEY')
# OpenAI Project ID
OPENAI_PROJECT_ID: str = env.str('OPENAI_PROJECT_ID')
# Temp dir location
TEMP_DIR: str = tempfile.gettempdir()


# Load app config (app_config.toml) file
with open('app_config.toml', mode='r', encoding='utf-8') as f:
    app_config = DefaultMunch.fromDict(load(f))


@dataclass(frozen=True)
class ChatTypes:
    """Telegram chat types."""
    private: str = 'private'
    group: str = 'group'
    supergroup: str = 'supergroup'
    channel: str = 'channel'
