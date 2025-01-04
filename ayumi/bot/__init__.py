from telebot.async_telebot import AsyncTeleBot

from ayumi.config import TELEGRAM_TOKEN


__all__ = (
    'start_ayumi',
    'session'
)


session = AsyncTeleBot(TELEGRAM_TOKEN)


def start_ayumi() -> None:
    """Use it to start telegram polling."""
    import asyncio

    asyncio.run(session.infinity_polling())


from .handlers import *
