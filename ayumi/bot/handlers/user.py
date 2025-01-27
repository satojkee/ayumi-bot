"""This module contains handlers for user commands."""


from typing import Callable

from telebot import types
from telebot.util import user_link

from ayumi.loc import get_translator, T
from ayumi.config import TELEGRAM_OWNER_ID, TELEGRAM_BOT_NAME
from ayumi.bot import session
from ayumi.bot.util import get_user
from ayumi.bot.misc import Command, ParseMode
from ayumi.bot.keyboard import access_keyboard
from ayumi.bot.decorators import auto_translator, trace_input


__all__ = ('help_handler', 'get_access_handler')


@session.message_handler(commands=Command.help + Command.start)
@auto_translator
@trace_input
async def help_handler(message: types.Message, _: Callable) -> None:
    """start + help commands handler.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    await session.send_message(
        chat_id=message.chat.id,
        text=_(T.Common.help).format(
            first_name=message.from_user.first_name,
            bot_name=TELEGRAM_BOT_NAME,
            get_access=Command.get_access[0]
        ),
        parse_mode=ParseMode.html
    )


@session.message_handler(commands=Command.get_access)
@auto_translator
@trace_input
async def get_access_handler(message: types.Message, _: Callable) -> None:
    """get_access command handler.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    tg_admin = await get_user(TELEGRAM_OWNER_ID)
    # create translator for admin based on preferred language
    admin_t = get_translator(tg_admin.language_code)
    # use `admin_t` for admin and `_` for user
    await session.reply_to(message=message, text=_(T.Access.pending))
    await session.send_message(
        chat_id=TELEGRAM_OWNER_ID,
        reply_markup=access_keyboard(chat_id=message.chat.id, t=_),
        parse_mode=ParseMode.html,
        text=admin_t(T.Common.access_request).format(
            chat_id=message.chat.id,
            user=user_link(message.from_user),
            title=message.chat.title,
            chat_type=message.chat.type
        )
    )
