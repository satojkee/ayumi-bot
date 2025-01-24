"""This module contains functions to work with OpenAI API."""


from io import BufferedReader

import openai

from ayumi.config import (
    OPENAI_SECRET_KEY,
    OPENAI_PROJECT_ID,
    app_config
)


__all__ = (
    'generate_text',
    'generate_image',
    'speech_to_text'
)


# currently using AsyncClient instead of common sync `Client`
client = openai.AsyncClient(api_key=OPENAI_SECRET_KEY,
                            project=OPENAI_PROJECT_ID)


async def generate_text(prompt: str) -> str:
    """Use it to generate an AI-text from a text prompt.

    :param prompt: str - input data
    :return: str - output data
    """
    response = await client.chat.completions.create(
        messages=[
            {'role': 'developer', 'content': app_config.openai.directive},
            {'role': 'user', 'content': prompt}
        ],
        **app_config.openai.text
    )

    return response.choices[0].message.content


async def generate_image(prompt: str) -> str:
    """Use it to generate an AI-image from a text prompt.

    :param prompt: str - input data
    :return: str - image url
    """
    response = await client.images.generate(prompt=prompt,
                                            **app_config.openai.image)

    return response.data[0].url


async def speech_to_text(handler: BufferedReader) -> str:
    """Use it to transcribe an audio file.

    :param handler: BufferedReader - audio file handler
    :return: str - extracted text
    """
    return await client.audio.transcriptions.create(
        **app_config.openai.speech_to_text,
        file=handler
    )
