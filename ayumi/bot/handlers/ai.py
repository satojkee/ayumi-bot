"""This module contains handlers that are related to OpenAI API."""


import os
from typing import Callable

from telebot import types

from ayumi.loc import T
from ayumi.bot import session
from ayumi.config import app_config, TEMP_DIR
from ayumi.api import generate_text, generate_image, speech_to_text
from ayumi.bot.misc import ParseMode, Pattern, ContentType
from ayumi.bot.decorators import trace_input, auth_required, auto_translator
from ayumi.bot.util import (
    extract_prompt,
    get_api_response,
    processing_message
)


__all__ = (
    'ai_text_handler',
    'ai_imagegen_handler',
    'ai_speech_to_text_handler',
    'ai_text_inline_handler'
)


@session.message_handler(content_types=ContentType.text,
                         regexp=Pattern.gen_text)
@auth_required(**app_config.security.ai.textgen)
@auto_translator
@trace_input
async def ai_text_handler(message: types.Message, _: Callable) -> None:
    """AI-text handler.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    pm_ = await processing_message(message, _)
    # wait for OpenAI API response
    response = await get_api_response(func=generate_text,
                                      prompt=extract_prompt(message))
    # edit `processing` message with generated response
    await session.edit_message_text(
        chat_id=message.chat.id,
        message_id=pm_.message_id,
        text=_(response),
        parse_mode=ParseMode.markdown
    )


@session.message_handler(content_types=ContentType.text,
                         regexp=Pattern.gen_image)
@auth_required(**app_config.security.ai.imagegen)
@auto_translator
@trace_input
async def ai_imagegen_handler(message: types.Message, _: Callable) -> None:
    """AI-image handler.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    pm_ = await processing_message(message, _)
    # wait for OpenAI API response
    response = await get_api_response(func=generate_image,
                                      prompt=extract_prompt(message))
    # send image if succeeded, else -> notify about error
    if response.startswith('https://'):
        # remove `T.Common.processing` message
        await session.delete_message(chat_id=message.chat.id,
                                     message_id=pm_.message_id)
        # send generated image
        await session.send_photo(
            chat_id=message.chat.id,
            photo=_(response),
            reply_to_message_id=message.message_id
        )
    else:
        await session.edit_message_text(
            chat_id=message.chat.id,
            message_id=pm_.message_id,
            text=_(response)
        )


@session.message_handler(content_types=ContentType.voice)
@auth_required(**app_config.security.ai.speech_to_text)
@auto_translator
@trace_input
async def ai_speech_to_text_handler(message: types.Message,
                                    _: Callable) -> None:
    """AI speech-to-text handler.

    :param message: types.Message - Message object
    :param _: Callable - translator func
    :return: None
    """
    pm_ = await processing_message(message, _)
    # processing voice file using `telebot` features
    # output file extension -> .ogg
    f_info = await session.get_file(message.voice.file_id)
    f_data = await session.download_file(f_info.file_path)
    # use '.ogg' for telegram voice files
    f_path = os.path.join(TEMP_DIR, f'{f_info.file_id}.ogg')

    with open(f_path, 'wb+') as handler:
        handler.write(f_data)
        # wait for OpenAI API response
        response = await get_api_response(func=speech_to_text,
                                          handler=handler)
    # replace `T.Common.processing` message with transcription
    await session.edit_message_text(
        chat_id=message.chat.id,
        message_id=pm_.message_id,
        text=_(response)
    )
    # remove file from temp
    os.remove(f_path)


@session.inline_handler(
    func=lambda q: len(q.query) > app_config.inline.query.min_len
)
@auth_required(**app_config.security.ai.textgen_inline)
@auto_translator
@trace_input
async def ai_text_inline_handler(query: types.InlineQuery,
                                 _: Callable) -> None:
    """AI-text inline handler.

    :param query: types.InlineQuery - InlineQuery object
    :param _: Callable - translator func
    :return: None
    """
    response = await get_api_response(func=generate_text,
                                      prompt=query.query)
    # answer inline query with response
    # set `cache_time=0`, because we don't need it
    await session.answer_inline_query(
        inline_query_id=query.id,
        cache_time=0,
        results=[
            types.InlineQueryResultArticle(
                id=query.id,
                description=_(response),
                title=_(T.Common.inline_title).format(query=query.query),
                input_message_content=types.InputTextMessageContent(
                    message_text=_(response)
                )
            )
        ]
    )
