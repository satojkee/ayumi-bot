import re
from typing import Callable, Any, Union

from telebot import types
from openai import BadRequestError

from ayumi import logger
from ayumi.bot import session
from ayumi.bot.props import T, Pattern


__all__ = (
    'get_api_response',
    'extract_prompt',
    'processing_message',
    'get_user'
)


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


async def get_api_response(func: Callable, *args: Any, **kwargs: Any) -> str:
    """OpenAI API request wrapper. Used to handle errors and format response.

    :param func: Callable - API request function
    :param args: Any - API request arguments
    :param kwargs: Any - API request keyword arguments
    :return: str - response as text
    """
    try:
        return await func(*args, **kwargs)
    except BadRequestError:
        logger.error('OpenAI aborted request due to bad params.')
    except Exception as e:
        logger.error(f'Unknown error raised during API request.', e)

    return T.Error.api


def extract_prompt(message: types.Message) -> str:
    """Use it to extract user's prompt from the message text.

    :param message: types.Message - Message object
    :return: str - user's prompt
    """
    return re.sub(Pattern.gen_request, '', message.text).strip()
