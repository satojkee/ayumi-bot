import telebot.types
from telebot.async_telebot import AsyncTeleBot

from . import TELEGRAM_TOKEN
from .requester import create_completion


# Const
BOT_NAME: str = 'Ayumi'

# Creating a session
session: AsyncTeleBot = AsyncTeleBot(TELEGRAM_TOKEN)


def extract_message(message: str) -> str:
    """
    This function extracts the message from the command.
    Divides the message with " " -> removes command -> generates message.

    :return: <str>
    """
    return ' '.join(message.split(' ')[1:])


@session.message_handler(content_types=['text'], func=lambda message: True)
async def text_handler(message: telebot.types.Message) -> None:
    # if response is required
    if message.text.startswith(BOT_NAME):
        response: str = await create_completion(extract_message(message.text))
        await session.reply_to(
            message=message,
            text=response
        )
