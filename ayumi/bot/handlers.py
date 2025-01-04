import re
from typing import Callable

from telebot.types import Message, CallbackQuery

from ayumi.loc import *
from ayumi.api import *
from ayumi.bot import session
from ayumi.bot.util import *
from ayumi.bot.props import *
from ayumi.bot.keyboard import *
from ayumi.db.repository import *
from ayumi.config import TELEGRAM_OWNER_ID, TELEGRAM_BOT_NAME


__all__ = (
    'request_access_handler',
    'access_callback',
    'ai_text_handler',
    'ai_imagegen_handler',
    'help_handler',
    'start_handler',
    'status_handler'
)


@session.message_handler(commands=Command.start)
@auto_translator
@trace_message
async def start_handler(message: Message, _: Callable) -> None:
    """Help command handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    await session.reply_to(
        message=message,
        text=_(T.Common.start).format(
            first_name=message.from_user.first_name,
            bot_name=TELEGRAM_BOT_NAME
        ),
        parse_mode=ParseMode.html
    )

    await help_handler(message)


@session.message_handler(commands=Command.help)
@auto_translator
@trace_message
async def help_handler(message: Message, _: Callable) -> None:
    """Help command handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    await session.send_message(
        chat_id=message.chat.id,
        text=_(T.Common.help).format(
            bot_name=TELEGRAM_BOT_NAME,
            request_access=Command.request_access[0],
            status=Command.status[0]
        ),
        parse_mode=ParseMode.html
    )


@session.message_handler(commands=Command.status)
@auto_translator
@trace_message
@authenticate
async def status_handler(message: Message, auth: bool, _: Callable) -> None:
    """Help command handler.

    :param message: Message - Message object
    :param auth: bool - user authentication status
    :param _: Callable - translator func
    :return: None
    """
    await session.send_message(
        chat_id=message.chat.id,
        text=_(T.Status.positive if auth else T.Status.negative).format(
            first_name=message.from_user.first_name
        ),
        parse_mode=ParseMode.html
    )


@session.message_handler(commands=Command.request_access)
@auto_translator
@trace_message
async def request_access_handler(message: Message, _: Callable) -> None:
    """request_access command handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    default_t = get_translator()
    # use default translator for admin and specific for user
    await session.reply_to(message=message, text=_(T.Common.request_pending))
    await session.send_message(
        chat_id=TELEGRAM_OWNER_ID,
        reply_markup=ad_keyboard(message.from_user.id, default_t),
        parse_mode=ParseMode.html,
        text=default_t(T.Common.access_request).format(
            username=message.from_user.username,
            uuid=message.from_user.id
        ),
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
            t(T.Common.access_granted)
            if state
            else
            t(T.Common.access_refused)
        )
    )
    await session.answer_callback_query(call.id)


@session.message_handler(
    content_types=ContentType.text,
    func=lambda message: re.match(Pattern.gen_text, message.text)
)
@trace_message
@auto_translator
@authenticate
async def ai_text_handler(message: Message, auth: bool, _: Callable) -> None:
    """AI text generation handler.
    AI request always starts with a name of the bot. Currently: `Ayumi`
    E.g: `Ayumi: Hello!`

    :param message: Message - Message object
    :param auth: bool - user authentication status
    :param _: Callable - translator func
    :return: None
    """
    if auth:
        await session.reply_to(message=message, text=_(T.Common.processing))
        # using `get_api_response` to handle API errors
        response = await get_api_response(
            func=generate_text,
            t=_,
            prompt=extract_prompt(message)
        )

        await session.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id + 1,
            text=response,
            parse_mode=ParseMode.markdown
        )
    else:
        await send_access_warning(message, _)


@session.message_handler(
    content_types=ContentType.text,
    func=lambda message: re.match(Pattern.gen_image, message.text)
)
@trace_message
@auto_translator
@authenticate
async def ai_imagegen_handler(message: Message,
                              auth: bool, _: Callable) -> None:
    """AI image generation handler.

    :param message: Message - Message object
    :param auth: bool - user authentication status
    :param _: Callable - translator func
    :return: None
    """
    if auth:
        await session.reply_to(message=message, text=_(T.Common.processing))
        # using `get_api_response` to handle API errors
        response = await get_api_response(
            func=generate_image,
            t=_,
            prompt=extract_prompt(message)
        )
        # `response` is a direct image url
        # reply to prompt message with generated image
        if response.startswith('https://'):
            await session.send_photo(
                chat_id=message.chat.id,
                photo=response,
                reply_to_message_id=message.message_id
            )
        else:
            await session.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id + 1,
                text=response
            )
    else:
        await send_access_warning(message, _)
