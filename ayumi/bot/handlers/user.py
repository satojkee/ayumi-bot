from typing import Callable

from telebot.types import Message

from ayumi.loc import *
from ayumi.bot import session
from ayumi.config import TELEGRAM_OWNER_ID, TELEGRAM_BOT_NAME
from ayumi.bot.util import *
from ayumi.bot.props import *
from ayumi.bot.keyboard import *


__all__ = (
    'help_handler',
    'request_access_handler'
)


@session.message_handler(commands=Command.help + Command.start)
@auto_translator
@trace_input
async def help_handler(message: Message, _: Callable) -> None:
    """Help command handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    await session.send_message(
        chat_id=message.chat.id,
        text=_(T.Common.help).format(
            first_name=message.from_user.first_name,
            bot_name=TELEGRAM_BOT_NAME,
            request_access=Command.request_access[0]
        ),
        parse_mode=ParseMode.html
    )


@session.message_handler(commands=Command.request_access)
@auto_translator
@trace_input
async def request_access_handler(message: Message, _: Callable) -> None:
    """request_access command handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    default_t = get_translator()
    # use default translator for admin and specific for user
    await session.reply_to(message=message, text=_(T.Access.pending))
    await session.send_message(
        chat_id=TELEGRAM_OWNER_ID,
        reply_markup=ad_keyboard(message.from_user.id, default_t),
        parse_mode=ParseMode.html,
        text=default_t(T.Common.access_request).format(
            username=message.from_user.username,
            uuid=message.from_user.id
        ),
    )
