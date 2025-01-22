import re
import functools
from typing import Callable, Any, Union

from telebot import types
from telebot.util import user_link
from openai import BadRequestError

from ayumi import logger
from ayumi.loc import get_translator
from ayumi.bot import session
from ayumi.db.repository import UserRepo
from ayumi.bot.props import T, ParseMode, Pattern
from ayumi.config import TELEGRAM_OWNER_ID, app_config


__all__ = (
    'get_api_response',
    'auto_translator',
    'trace_input',
    'authenticate',
    'extract_prompt',
    'processing_prompt_message',
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


async def processing_prompt_message(message: types.Message,
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


def auto_translator(func: Callable) -> Any:
    """Use it as decorator for telebot handlers.
    Automatically identifies preferred language and injects proper translator.

    Usage:
        @bot.message_handler(...)
        @auto_translator
        def my_handler(message: types.Message, _: Callable) -> None:
            _('my.translation') # returns a translated string (IF provided)

    :return: Any
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        message = args[0]

        return await func(_=get_translator(message.from_user.language_code),
                          *args, **kwargs)

    return wrapper


def trace_input(func: Callable) -> Any:
    """Use it as decorator for telebot handlers.
    Apply for each handler you want to see user input from.

    Usage:
        @bot.message_handler(...)
        @trace_input
        def my_handler(message: types.Message, ...) -> None:
           ...

    :return: Any
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        input_ = args[0]
        # decorated handler usually has first param as API response model
        # that model we're looking for
        logger.info(f'input received: {input_.__class__.__name__}({input_})')

        return await func(*args, **kwargs)

    return wrapper


def authenticate(level: int = app_config.security.default) -> Any:
    """Use it as decorator for telebot handlers.
    Apply for each handler where user authentication is required.

    Usage:
        @bot.message_handler(...)
        @authenticate(level=...)
        def my_handler(message: types.Message, ...) -> None:
           ...

    :param level: int - minimal required access level
    :return: Any
    """
    def decorator(func: Callable) -> Any:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            tg_user = args[0].from_user
            # create proper translator
            t = get_translator(tg_user.language_code)

            if level not in app_config.security.levels:
                logger.warning(
                    f'undefined access level: "{level}" in "{func.__name__}"'
                )
                # send error message in telegram
                await session.send_message(chat_id=tg_user.id,
                                           text=t(T.Error.auth))
            else:
                # admin is always authenticated
                # if not admin, check access level
                auth = tg_user.id == TELEGRAM_OWNER_ID
                if not auth:
                    user_ = await UserRepo.get(uuid=tg_user.id)
                    auth = user_ is not None and user_.level >= level

                if auth:
                    return await func(*args, **kwargs)
                else:
                    tg_admin = await get_user(TELEGRAM_OWNER_ID)
                    # send `T.Error.permissions` message
                    # with administrator link
                    await session.send_message(
                        chat_id=tg_user.id,
                        parse_mode=ParseMode.html,
                        text=(
                            t(T.Error.permissions)
                            .format(admin=user_link(tg_admin))
                        )
                    )

        return wrapper

    return decorator
