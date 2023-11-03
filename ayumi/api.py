from telebot.async_telebot import AsyncTeleBot

from .messages import *
from . import TELEGRAM_TOKEN, BOT_NAME, logger
from .requester import create_completion


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
async def text_handler(message) -> None:
    """
    This function handles each message.
    It responds only if the message starts with the bot name.
    Other messages are ignored.

    :param message: <Message>
    :return: <None>
    """
    if message.text.startswith(BOT_NAME):
        query: str = extract_message(message.text)
        response: str = await create_completion(query)

        if isinstance(response, str):
            await session.reply_to(message=message, text=response)

            logger.info(INFO_RESPONSE_SENT.format(
                message.chat.id,
                message.from_user.id,
                query,
                response
            ))
        else:
            await session.reply_to(message=message, text=CHAT_RESPONSE_FAILED)

            logger.error(ERROR_REQUEST_FAILED.format(
                message.chat.id,
                message.from_user.id,
                query,
                response
            ))
