import os
from typing import Callable

from telebot.types import (
    Message,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from ayumi.bot import session
from ayumi.api import *
from ayumi.bot.util import *
from ayumi.bot.props import *
from ayumi.config import app_config


__all__ = (
    'ai_text_handler',
    'ai_imagegen_handler',
    'ai_speech_to_text_handler',
    'ai_text_inline_handler'
)


@session.message_handler(content_types=ContentType.text,
                         regexp=Pattern.gen_text)
@authenticate()
@auto_translator
@trace_input
async def ai_text_handler(message: Message, _: Callable) -> None:
    """AI-text handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    pm_ = await processing_prompt_message(message, _)
    # wait for OpenAI API response
    response = await get_api_response(
        func=generate_text,
        t=_,
        prompt=extract_prompt(message)
    )
    # edit `processing` message with generated response
    await session.edit_message_text(
        chat_id=message.chat.id,
        message_id=pm_.message_id,
        text=response,
        parse_mode=ParseMode.markdown
    )


@session.message_handler(content_types=ContentType.text,
                         regexp=Pattern.gen_image)
@authenticate()
@auto_translator
@trace_input
async def ai_imagegen_handler(message: Message, _: Callable) -> None:
    """AI-image handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    pm_ = await processing_prompt_message(message, _)
    # wait for OpenAI API response
    response = await get_api_response(
        func=generate_image,
        t=_,
        prompt=extract_prompt(message)
    )
    # send image if succeeded, else -> notify about error
    if response.startswith('https://'):
        # remove `T.Common.processing` message
        await session.delete_message(chat_id=message.chat.id,
                                     message_id=pm_.message_id)
        # send generated image
        await session.send_photo(
            chat_id=message.chat.id,
            photo=response,
            reply_to_message_id=message.message_id
        )
    else:
        await session.edit_message_text(
            chat_id=message.chat.id,
            message_id=pm_.message_id,
            text=response
        )


@session.message_handler(content_types=ContentType.voice)
@authenticate()
@auto_translator
@trace_input
async def ai_speech_to_text_handler(message: Message, _: Callable) -> None:
    """AI speech-to-text handler.

    :param message: Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    pm_ = await processing_prompt_message(message, _)
    # processing voice file using `telebot` features
    # output file extension -> .ogg
    f_info = await session.get_file(message.voice.file_id)
    f_data = await session.download_file(f_info.file_path)
    f_path = os.path.join(app_config.common.temp, f'{f_info.file_id}.ogg')

    with open(f_path, 'wb+') as handler:
        handler.write(f_data)
        # wait for OpenAI API response
        response = await get_api_response(
            func=speech_to_text,
            t=_,
            handler=handler
        )
    # replace `T.Common.processing` message with extracted text
    await session.edit_message_text(
        chat_id=message.chat.id,
        message_id=pm_.message_id,
        text=response
    )
    # remove file from temp
    os.remove(f_path)


@session.inline_handler(
    func=lambda q: len(q.query) > app_config.inline.query.min_len
)
@authenticate()
@auto_translator
@trace_input
async def ai_text_inline_handler(query: InlineQuery, _: Callable) -> None:
    """AI-text inline handler.

    :param query: InlineQuery - InlineQuery object
    :param _: Callable - translator func
    :return: None
    """
    response = await get_api_response(
        func=generate_text,
        t=_,
        prompt=query.query
    )
    # answer inline query with response
    await session.answer_inline_query(
        inline_query_id=query.id,
        cache_time=0,
        results=[
            InlineQueryResultArticle(
                id=query.id,
                description=response,
                title=_(T.Common.inline_title).format(query=query.query),
                input_message_content=InputTextMessageContent(
                    message_text=response,
                    parse_mode=ParseMode.markdown
                )
            )
        ]
    )
