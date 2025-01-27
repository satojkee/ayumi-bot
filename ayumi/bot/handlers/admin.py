"""This module contains ADMIN ONLY features."""


import re
from typing import Callable

from telebot import types
from telebot.util import antiflood, extract_command

from ayumi.bot import session
from ayumi.loc import get_translator, T
from ayumi.config import app_config, ChatTypes
from ayumi.db.repository import ChatRepo, ChatTypeRepo
from ayumi.bot.util import parse_access_callback
from ayumi.bot.misc import ParseMode, Pattern, Command
from ayumi.bot.keyboard import access_keyboard
from ayumi.bot.decorators import trace_input, auth_required, auto_translator


__all__ = ('access_callback', 'get_chats_handler')


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
    chat_id, level = parse_access_callback(call)
    if level != app_config.security.zero:
        tg_chat = await session.get_chat(chat_id=chat_id)
        # chat type from the db
        chat_type_ = await ChatTypeRepo.get(name=tg_chat.type)
        # create or update an existing chat in the db
        await ChatRepo.update(
            chat_id=chat_id,
            title=tg_chat.title,
            chat_type=chat_type_,
            level=level
        )
    else:
        await ChatRepo.delete(chat_id=chat_id)

    # send notification to the chat
    t = get_translator()
    await session.send_message(
        chat_id=chat_id,
        parse_mode=ParseMode.html,
        text=t(T.Access.granted
               if level != app_config.security.zero
               else T.Access.refused).format(level=level)
    )
    await session.answer_callback_query(callback_query_id=call.id)
    await session.delete_message(chat_id=call.from_user.id,
                                 message_id=call.message.id)


@session.message_handler(commands=Command.users + Command.groups)
@auth_required(admin_only=True)
@auto_translator
@trace_input
async def get_chats_handler(message: types.Message, _: Callable) -> None:
    """Fetches a list of users from the database.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    command = extract_command(message.text)
    # type name depends on command
    type_name = ChatTypes.private \
        if command in Command.users \
        else ChatTypes.group
    # fetch chat type from the db to use its id as filter for `Chat` instances
    chat_type = await ChatTypeRepo.get(name=type_name)
    for chat_ in await ChatRepo.get_all(chat_type_id=chat_type.id):
        await antiflood(
            function=session.send_message,
            chat_id=message.from_user.id,
            text=_(T.Common.chat_profile).format(
                chat_id=chat_.chat_id,
                title=chat_.title,
                chat_type=type_name,
                created=chat_.created
            ),
            reply_markup=access_keyboard(
                chat_id=chat_.chat_id,
                highlight=chat_.level,
                t=_
            ),
            parse_mode=ParseMode.html
        )
