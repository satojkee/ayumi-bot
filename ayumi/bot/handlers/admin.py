import re
from typing import Callable

from telebot.util import user_link, antiflood
from telebot.types import Message, CallbackQuery

from ayumi.bot import session
from ayumi.loc import *
from ayumi.bot.util import *
from ayumi.bot.props import *
from ayumi.bot.keyboard import *
from ayumi.db.repository import *
from ayumi.config import TELEGRAM_OWNER_ID


__all__ = (
    'access_callback',
    'get_users_handler'
)


@session.callback_query_handler(
    func=lambda call: re.match(Pattern.access, call.data)
)
async def access_callback(call: CallbackQuery) -> None:
    """Callback query handler.
    Access approve/deny and revoke handler.

    :param call: CallbackQuery - CallbackQuery object
    :return: None
    """
    uuid, state = [int(i) for i in call.data.split(':')]
    # this is required to get user's language code
    u_data = await session.get_chat_member(uuid, uuid)
    # generating proper translator
    t = get_translator(u_data.user.language_code)

    if state:
        await UserRepo.create(uuid=uuid)
        # change `A/D` keyboard with `Revoke` one
        await session.edit_message_reply_markup(
            chat_id=TELEGRAM_OWNER_ID,
            message_id=call.message.id,
            reply_markup=revoke_keyboard(uuid, get_translator())
        )
    else:
        await UserRepo.delete(uuid=uuid)
        # remove message from the admin chat
        await session.delete_message(
            chat_id=TELEGRAM_OWNER_ID,
            message_id=call.message.id
        )
    # inform the user about the result of operation
    await session.send_message(
        chat_id=uuid,
        text=(
            t(T.Access.granted)
            if state
            else
            t(T.Access.refused)
        )
    )
    await session.answer_callback_query(call.id)


@session.message_handler(commands=Command.users)
@authenticate(admin_only=True)
@auto_translator
@trace_input
async def get_users_handler(message: Message, _: Callable) -> None:
    """Fetches a list of users from the database.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    for user_ in await UserRepo.get_all():
        udata = await session.get_chat_member(user_.uuid, user_.uuid)
        # use `antiflood` util to avoid telegram API violations
        await antiflood(
            function=session.send_message,
            chat_id=message.chat.id,
            reply_markup=revoke_keyboard(user_.uuid, _),
            parse_mode=ParseMode.html,
            text=_(T.Common.user_profile).format(
                user=user_link(udata.user), created=user_.created
            )
        )
