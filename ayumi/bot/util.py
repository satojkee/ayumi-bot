import re
import functools
from typing import Callable, Any, Optional

from telebot.types import Message
from openai import BadRequestError

from ayumi import logger
from ayumi.loc import get_translator
from ayumi.bot import session
from ayumi.db.repository import UserRepo
from ayumi.bot.props import T, ParseMode, Pattern
from ayumi.config import TELEGRAM_OWNER_ID, TELEGRAM_OWNER_USERNAME


__all__ = (
    'get_api_response',
    'auto_translator',
    'trace_message',
    'authenticate',
    'extract_prompt'
)


async def get_api_response(func: Callable, t: Callable,
                           *args: Any, **kwargs: Any) -> str:
    """OpenAI APi request wrapper. Used to handle errors and format response.

    :param func: Callable - API request function
    :param t: Callable - translator func
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

    return t(T.Error.api)


def auto_translator(func: Callable) -> Any:
    """Use it as decorator for telebot handlers.
    Automatically identifies preferred language and injects proper translator.

    Usage:
        @bot.message_handler(...)
        @auto_translator
        def my_handler(message: Message, _: Any) -> None:
            _('my.translation') # returns a translated string (IF provided)

    :return: Any
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        message = args[0]

        return await func(_=get_translator(message.from_user.language_code),
                          *args, **kwargs)

    return wrapper


def trace_message(func: Callable) -> Any:
    """Use it as decorator for telebot handlers.
    Apply for each handler you want to see messages from.

    Usage:
        @bot.message_handler(...)
        @trace_message
        def my_handler(message: Message, ...) -> None:
           ...

    :return: Any
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        message = args[0]

        if isinstance(message, Message):
            logger.info(f'received message: {message}')

        return await func(*args, **kwargs)

    return wrapper


def authenticate(admin_only: Optional[bool] = False) -> Any:
    """Use it as decorator for telebot handlers.
    Apply for each handler where user authentication is required.

    Usage:
        @bot.message_handler(...)
        @authenticate
        def my_handler(message: Message, auth: bool, ...) -> None:
           ...

    :return: Any
    """
    def decorator(func: Callable) -> Any:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            uuid = args[0].from_user.id
            # check if user is the admin
            # if not, and admin_only flag is set to `False` -> check in db
            auth = uuid == TELEGRAM_OWNER_ID
            if not admin_only:
                auth = auth or await UserRepo.get(uuid=uuid)
            # if user is authenticated -> decorated function
            # if not -> permissions violation
            if auth:
                return await func(*args, **kwargs)
            else:
                await session.send_message(
                    chat_id=uuid,
                    parse_mode=ParseMode.html,
                    text=(
                        get_translator(args[0].from_user.language_code)
                        (T.Error.permissions)
                        .format(admin=TELEGRAM_OWNER_USERNAME)
                    )
                )

        return wrapper

    return decorator


def extract_prompt(message: Message) -> str:
    """Use it to extract user's prompt from the message text.

    :param message: Message - Message object
    :return: str - user's prompt
    """
    return re.sub(Pattern.gen_request, '', message.text).strip()
