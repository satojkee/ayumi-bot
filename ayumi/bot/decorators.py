"""This module contains useful decorators for telebot handlers."""


import logging
import functools
from typing import Callable, Any, Optional

from telebot import types

from ayumi.loc import get_translator, T
from ayumi.config import app_config, TELEGRAM_OWNER_ID, ChatTypes
from ayumi.db.repository import ChatRepo
from ayumi.bot import session
from ayumi.bot.util import permissions_violation


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
                  admin_only: Optional[bool] = False,
                  allow_groups: Optional[bool] = False) -> Any:
    """Use it as decorator for telebot handlers.
    Apply for each handler where user authorization is required.

    Usage:
        @bot.message_handler(...)
        @auth_required(level=..., admin_only=..., allow_groups=...)
        @...
        def my_handler(message: types.Message, ...) -> None:
           ...

    :param level: int - minimal required access level
    :param admin_only: Optional[bool] - if True, only admin can access
    :param allow_groups: Optional[bool] - if True, any group member can access
    :return: Any
    """
    def decorator(func: Callable) -> Any:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async def _send_violation() -> None:
                """Wrapped function to not duplicate params."""
                return await permissions_violation(
                    chat_id=tg_input.from_user.id,
                    _=tg_user_t
                )

            tg_input = args[0]
            # generate proper translator function for the user
            tg_user_t = get_translator(tg_input.from_user.language_code)

            if level not in app_config.security.levels and not admin_only:
                logger.warning('undefined access level: "%s" in "%s"',
                               level, func.__name__)
                # notify user about the error
                await session.send_message(chat_id=tg_input.from_user.id,
                                           text=tg_user_t(T.Error.auth))
            else:
                auth = TELEGRAM_OWNER_ID == tg_input.from_user.id
                if not admin_only and not auth:
                    # for `CallbackQuery` instance use user's own id
                    # for `Message` instance use chat/user id depending on
                    # the `allow_groups` flag
                    if isinstance(tg_input, types.Message):
                        is_group = tg_input.chat.type == ChatTypes.group
                    else:
                        is_group = False

                    # is_group + allow_groups -> use chat id
                    # is_group + !allow_groups -> error
                    # !is_group -> use telegram user id
                    if is_group:
                        if allow_groups:
                            id_ = tg_input.chat.id
                        else:
                            return await _send_violation()
                    else:
                        id_ = tg_input.from_user.id

                    # get chat from the db
                    chat_ = await ChatRepo.get(chat_id=str(id_))
                    # check if user or group is valid
                    # and has the same or higher access level
                    auth = chat_ is not None and chat_.level >= level

                if auth:
                    return await func(*args, **kwargs)
                return await _send_violation()

        return wrapper

    return decorator
