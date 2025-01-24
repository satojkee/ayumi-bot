"""Contains all pyTelegramBotAPI related stuff."""


import json

from telebot.async_telebot import AsyncTeleBot

from ayumi.config import TELEGRAM_TOKEN, app_config


__all__ = ('start_ayumi', 'session')


session = AsyncTeleBot(TELEGRAM_TOKEN)


def start_ayumi() -> None:
    """Use it to start telegram polling."""
    import asyncio
    import logging

    logger = logging.getLogger(__name__)

    logger.debug(f'starting %s', __name__)
    logger.debug(f'running configuration: %s',
                 json.dumps(app_config, indent=2))

    asyncio.run(session.infinity_polling())


from .handlers import *
