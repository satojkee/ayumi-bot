"""This module contains useful decorators for telebot handlers."""


import logging
import functools
from typing import Callable, Any, Optional

from telebot.util import user_link

from ayumi.loc import get_translator
from ayumi.config import app_config, TELEGRAM_OWNER_ID
from ayumi.db.repository import UserRepo
from ayumi.bot import session
from ayumi.bot.util import get_user
from ayumi.bot.props import ParseMode, T


__all__ = ('auth_required', 'trace_input', 'auto_translator')


logger = logging.getLogger(__name__)


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
        language_code = args[0].from_user.language_code
        # return function with injected translator
        return await func(_=get_translator(language_code), *args, **kwargs)

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
        # decorated handler always has a response model as first argument
        # that model we're looking for
        logger.info('input received: %s(%s)',
                    input_.__class__.__name__, input_)

        return await func(*args, **kwargs)

    return wrapper


def auth_required(level: Optional[int] = None,
                  admin_only: Optional[bool] = False) -> Any:
    """Use it as decorator for telebot handlers.
    Apply for each handler where user authorization is required.

    Usage:
        @bot.message_handler(...)
        @auth_required(level=..., admin_only=...)
        def my_handler(message: types.Message, ...) -> None:
           ...

    :param level: int - minimal required access level
    :param admin_only: Optional[bool] - if True, only admin can access
    :return: Any
    """
    def decorator(func: Callable) -> Any:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            tg_user = args[0].from_user
            tg_user_t = get_translator(tg_user.language_code)

            if level not in app_config.security.levels and not admin_only:
                logger.warning('undefined access level: "%s" in "%s"',
                               level, func.__name__)
                # notify user about the error
                await session.send_message(chat_id=tg_user.id,
                                           text=tg_user_t(T.Error.auth))
            else:
                # administrator is always authorized
                auth = tg_user.id == TELEGRAM_OWNER_ID
                if not auth and not admin_only:
                    user_ = await UserRepo.get(uuid=tg_user.id)
                    # check security level, it should be the same or higher
                    # than a required one to pass
                    auth = user_ is not None and user_.level >= level

                # if everything is fine -> pass the func
                if auth:
                    return await func(*args, **kwargs)
                # otherwise, access violation
                tg_admin = await get_user(TELEGRAM_OWNER_ID)
                # send `T.Error.permissions` message
                # with administrator link
                await session.send_message(
                    chat_id=tg_user.id,
                    parse_mode=ParseMode.html,
                    text=(
                        tg_user_t(T.Error.permissions)
                        .format(admin=user_link(tg_admin))
                    )
                )

        return wrapper

    return decorator
