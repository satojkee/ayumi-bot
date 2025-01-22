import re
from typing import Callable

from telebot import types
from telebot.util import user_link, antiflood

from ayumi.bot import session
from ayumi.loc import *
from ayumi.bot.util import *
from ayumi.bot.props import *
from ayumi.bot.keyboard import *
from ayumi.db.repository import *
from ayumi.config import app_config


__all__ = (
    'access_callback',
    'get_users_handler'
)


@session.callback_query_handler(
    func=lambda call: re.match(Pattern.access, call.data)
)
@trace_input
async def access_callback(call: types.CallbackQuery) -> None:
    """Callback query handler.
    Access management system controller.

    :param call: types.CallbackQuery - CallbackQuery object
    :return: None
    """
    uuid, level = [int(i) for i in call.data.split(':')]
    # this is required to get user's language code
    tg_user = await get_user(uuid)
    # generating proper translator
    t = get_translator(tg_user.language_code)

    if level != app_config.security.zero:
        await UserRepo.update(uuid=uuid, level=level)
    else:
        await UserRepo.delete(uuid=uuid)

    # notify user about the decision
    await session.send_message(
        chat_id=uuid,
        parse_mode=ParseMode.html,
        text=t(T.Access.granted
               if level != app_config.security.zero
               else T.Access.refused).format(level=level)
    )
    await session.answer_callback_query(callback_query_id=call.id)
    await session.delete_message(chat_id=call.from_user.id,
                                 message_id=call.message.id)


@session.message_handler(commands=Command.users)
@authenticate(level=app_config.security.levels[-1])
@auto_translator
@trace_input
async def get_users_handler(message: types.Message, _: Callable) -> None:
    """Fetches a list of users from the database.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    for user_ in await UserRepo.get_all():
        tg_user = await get_user(user_.uuid)
        # use `antiflood` util to avoid telegram API violations
        await antiflood(
            function=session.send_message,
            chat_id=message.chat.id,
            parse_mode=ParseMode.html,
            reply_markup=access_keyboard(
                uuid=user_.uuid,
                highlight=user_.level,
                t=_
            ),
            text=_(T.Common.user_profile).format(
                user=user_link(tg_user),
                created=user_.created
            )
        )
