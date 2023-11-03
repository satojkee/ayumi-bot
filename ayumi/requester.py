import openai
from typing import Union

from . import OPENAI_TOKEN, AI_MODEL, INSTRUCTIONS


# Configuring API key
openai.api_key = OPENAI_TOKEN


async def create_completion(data: str) -> Union[str, Exception]:
    """
    This function creates request to openai AI model.

    Returns model response as string.

    :param data: <str> -> input data.
    :return: <str> -> AI processed data (response).
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model=AI_MODEL,
            messages=[
                {'role': 'system', 'content': INSTRUCTIONS},
                {'role': 'user', 'content': data}
            ]
        )
    except Exception as e:
        return e

    return response.choices[0].message.content
