import openai

from ayumi.config import (
    OPENAI_SECRET_KEY,
    OPENAI_PROJECT_ID,
    app_config
)


__all__ = ('generate_text', 'generate_image')


client = openai.AsyncClient(
    api_key=OPENAI_SECRET_KEY,
    project=OPENAI_PROJECT_ID
)


async def generate_text(prompt: str) -> str:
    """Use it to make a request to OpenAI API to get AI-response.

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
    response = await client.images.generate(
        prompt=prompt,
        **app_config.openai.image
    )

    return response.data[0].url
