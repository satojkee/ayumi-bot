"""This module contains useful functions to use in handlers."""


import re
import logging
from typing import Callable, Any, Union

from telebot import types
from telebot.util import user_link

from ayumi.config import TELEGRAM_OWNER_ID
from ayumi.loc import T
from ayumi.bot import session
from ayumi.bot.misc import Pattern, ParseMode


__all__ = (
    'get_api_response',
    'extract_prompt',
    'processing_message',
    'get_user',
    'parse_access_callback',
    'permissions_violation'
)


logger = logging.getLogger(__name__)


async def get_user(uuid: Union[int, str]) -> types.User:
    """Use it to get a `types.User` instance by its telegram id.

    There's no a direct way to get `User` instance by its telegram id, using
        API provided by telegram.
    It's kinda abuse to get a chat member of a private chat (not a group)
        and extract a `types.User` instance from a `types.ChatMember` instance.

    :param uuid: Union[int, str] - user's telegram id
    :return: types.User - `types.User` instance
    """
    cm = await session.get_chat_member(uuid, uuid)

    return cm.user


async def processing_message(message: types.Message,
                             _: Callable) -> types.Message:
    """Reply to message with `T.Common.processing`.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    return await session.reply_to(message=message,
                                  text=_(T.Common.processing))


async def permissions_violation(chat_id: int, _: Callable) -> None:
    """Send a `T.Error.permissions` message to the user in a private chat.

    :param chat_id: int - telegram chat id
    :param _: Callable - translator func
    :return: None
    """
    tg_admin = await get_user(TELEGRAM_OWNER_ID)
    # send message to the user
    await session.send_message(
        chat_id=chat_id,
        parse_mode=ParseMode.html,
        text=_(T.Error.permissions).format(admin=user_link(tg_admin))
    )


async def get_api_response(func: Callable, *args: Any, **kwargs: Any) -> str:
    """OpenAI API request wrapper. Used to handle errors and format response.

    :param func: Callable - function
    :param args: Any - API request arguments
    :param kwargs: Any - API request keyword arguments
    :return: str - response as text
    """
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        logger.error('something went wrong during API request, %s', e)

    return T.Error.api


def extract_prompt(message: types.Message) -> str:
    """Use it to extract user's prompt from the message text.

    :param message: types.Message - Message object
    :return: str - user's prompt
    """
    return re.sub(Pattern.gen_request, '', message.text).strip()


def parse_access_callback(call: types.CallbackQuery) -> tuple[str, int]:
    """Use it to parse access callback data.

    :param call: types.CallbackQuery - CallbackQuery instance
    :return: tuple[str, int] - chat_id, level
    """
    as_list = call.data.split(':')

    return as_list[0], int(as_list[1])
