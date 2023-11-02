import openai

from . import OPENAI_TOKEN, AI_MODEL


# Configuring API key
openai.api_key = OPENAI_TOKEN


async def create_completion(data: str) -> str:
    """
    This function creates request to openai AI model.

    Returns model response as string.

    :param data: <str> -> input data.
    :return: <str> -> AI processed data (response).
    """
    response = await openai.ChatCompletion.acreate(
        model=AI_MODEL,
        messages=[{
            "role": "user",
            "content": data
        }]
    )

    return response.choices[0].message.content
