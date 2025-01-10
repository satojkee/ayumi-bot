from typing import Callable

from telebot.types import Message

from ayumi.bot import session
from ayumi.api import *
from ayumi.bot.util import *
from ayumi.bot.props import *


__all__ = (
    'ai_text_handler',
    'ai_imagegen_handler'
)


async def processing_prompt_message(message: Message, _: Callable) -> None:
    """Reply to message with `T.Common.processing`.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    await session.reply_to(message=message, text=_(T.Common.processing))


@session.message_handler(content_types=ContentType.text,
                         regexp=Pattern.gen_text)
@authenticate()
@auto_translator
async def ai_text_handler(message: Message, _: Callable) -> None:
    """AI-text handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    await processing_prompt_message(message, _)
    # wait for OpenAI response
    response = await get_api_response(
        func=generate_text,
        t=_,
        prompt=extract_prompt(message)
    )
    # edit `processing` message with generated response
    await session.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id + 1,
        text=response,
        parse_mode=ParseMode.markdown
    )


@session.message_handler(content_types=ContentType.text,
                         regexp=Pattern.gen_image)
@authenticate()
@auto_translator
@trace_message
async def ai_imagegen_handler(message: Message, _: Callable) -> None:
    """AI-image handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    await processing_prompt_message(message, _)
    # wait for OpenAI response
    response = await get_api_response(
        func=generate_image,
        t=_,
        prompt=extract_prompt(message)
    )
    # send image if succeeded, else -> notify about error
    if response.startswith('https://'):
        # remove `T.Common.processing` message
        await session.delete_message(chat_id=message.chat.id,
                                     message_id=message.message_id + 1)
        # send generated image
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
