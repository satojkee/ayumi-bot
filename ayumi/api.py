import openai

from ayumi.config import (
    OPENAI_SECRET_KEY,
    OPENAI_PROJECT_ID,
    OPENAI_TEXT_MODEL,
    OPENAI_IMAGE_MODEL,
    OPENAI_MODEL_INSTRUCTIONS,
    app_config
)


__all__ = ('generate_text', 'generate_image')


client = openai.AsyncClient(
    api_key=OPENAI_SECRET_KEY,
    project=OPENAI_PROJECT_ID
)


async def generate_text(prompt: str, model: str = OPENAI_TEXT_MODEL) -> str:
    """Use it to make a request to OpenAI API to get AI-response.

    :param prompt: str - input data
    :param model: str - model to use (OPENAI_TEXT_MODEL by default)
    :return: str - output data
    """
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'developer', 'content': OPENAI_MODEL_INSTRUCTIONS},
            {'role': 'user', 'content': prompt}
        ]
    )

    return response.choices[0].message.content


async def generate_image(prompt: str, model: str = OPENAI_IMAGE_MODEL) -> str:
    """Use it to generate an AI-image from a text prompt.

    :param prompt: str - input data
    :param model: str - model to use (OPENAI_IMAGE_MODEL by default)
    :return: str - image url
    """
    response = await client.images.generate(
        prompt=prompt,
        model=model,
        **app_config.openai.image
    )

    return response.data[0].url
