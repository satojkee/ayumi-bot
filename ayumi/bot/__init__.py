import json

from telebot.async_telebot import AsyncTeleBot

from ayumi import logger
from ayumi.config import TELEGRAM_TOKEN, app_config


__all__ = (
    'start_ayumi',
    'session'
)


session = AsyncTeleBot(TELEGRAM_TOKEN)


def start_ayumi() -> None:
    """Use it to start telegram polling."""
    import asyncio

    logger.debug(f'starting {__name__}')
    logger.debug(f'running configuration: {json.dumps(app_config, indent=2)}')

    asyncio.run(session.infinity_polling())


from .handlers import *
