# Ayumi - Chat-GPT powered telegram bot

[![BotPicture](https://i.imgur.com/dh6PRx9.png)](https://t.me/myAyumi_bot)

* Author: [satojkee](https://github.com/satojkee/)
* Project: [ayumi-bot](https://github.com/satojkee/ayumi-bot/)
* Production: [AyumiBot](https://t.me/myAyumi_bot)

> Production version is secured and won't allow you to use AI features without authorization. 


---


## Features

- Text generation ✔️
- Image generation ✔️
- Speech-to-text ✔️
- Inline mode support ✔️
- Private chat support ✔️
- Access management system with different levels of access ✔️
- Group chat support ✔️
- [Deepseek](https://www.deepseek.com/) support `coming soon`

<img alt="preview" src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExb282OXY5eHI2Z25kOXRzY2RneWI4amszeTV3cHY2anlqN3dib3FkdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VmfOoHbB3rzhHpvsRe/giphy.gif" />


## Useful links

* [OpenAI API docs](https://platform.openai.com/docs/overview)
* [pyTelegramBotAPI](https://pytba.readthedocs.io/en/latest/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [BotFather](https://telegram.me/BotFather)
* [GetIDsBot](https://t.me/getidsbot)
* [PyBabel](https://babel.pocoo.org/en/latest/)
* [PostgreSQL](https://www.postgresql.org/download/)


## Usage guide

### Clone repository

```shell
git clone https://github.com/satojkee/ayumi-bot.git
```


### Install dependencies

```shell
pip3 install -r requirements.txt
```


### Configure environment variables

> Set each property using `.env` file or via `cli`

#### Required variables

| Variable            | Description          | Hint                                                                                                                                   |
|---------------------|----------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `DATABASE_URI`      | Database credentials | PostgreSQL + asyncpg, format: `postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}` |
| `TELEGRAM_TOKEN`    | Telegram bot token   | visit [BotFather](https://t.me/BotFather) and create your own bot                                                                      |
| `TELEGRAM_OWNER_ID` | Telegram admin id    | use [GetIDsBot](https://t.me/getidsbot) to get your account id                                                                         |
| `TELEGRAM_BOT_NAME` | Telegram bot name    | this name is used as filter for prompts, e.g: `TELEGRAM_BOT_NAME, hello!` or `TELEGRAM_BOT_NAME@i, image of a cute kitten.`            |
| `OPENAI_PROJECT_ID` | OpenAI project ID    | visit [OpenAI](https://platform.openai.com/settings/organization/projects) and create a new project                                    |
| `OPENAI_SECRET_KEY` | OpenAI API token     | create a new `API-KEY` for a created project on OpenAI platform                                                                        |

#### Additional variables

> Used in [docker-compose](#docker-compose-postgresql--ayumibot) case, don't forget to build a `DATABASE_URI` in proper way \
> Example: `postgresql+asyncpg://postgres:postgres_secret@postgres:5432/test_database`

| Variable            | Description       | Hint                          |
|---------------------|-------------------|-------------------------------|
| `POSTGRES_USER`     | Database user     | `postgres` for example        |
| `POSTGRES_PASSWORD` | Database password | `postgres_secret` for example |
| `POSTGRES_DB`       | Database name     | `test_database` for example   |


### Edit `app_config.toml` if needed (optional)

> For example, you can replace the `gpt-4o-mini` text-model with `gpt-3.5-turbo` or `gpt-4o`, **but don't forget to enable this model in your project settings on OpenAI platform**
> 
> ### Explanation
>
> * `security`
>   * **levels** - a list of supported security levels in ascending order
>   * **zero** - this value is used in **keyboard.access_keyboard** and **handlers.admin.access_callback** to represent negative access response
>
> * `security.ai` - currently supports **level** and **allow_groups** params
>   * **textgen** - text generation
>   * **textgen_inline** - text generation in inline mode
>   * **speech_to_text** - speech-to-text
>   * **imagegen** - image generation
> 
> * `inline.query`
>   * **min_len** - min length of a prompt in **inline mode**
> 
> * `locale`
>   * **languages** - a list of supported languages
> 
> * `logger`
>   * **level** - logger level, supported levels: 
>     - **DEBUG** - `default`
>     - **INFO**
>     - **WARNING**
>     - **ERROR**
>     - **CRITICAL**
> * `openai`
>   * **directive** - Answers the question: "How to act?", for **textgen** and **textgen_inline**
> * `locale.translator` - supports all **gettext.translation** function params
> * `openai.text` - supports all **openai.client.chat.completion.create** function params
> * `openai.image` - supports all **openai.client.images.generate** function params
> * `openai.speech_to_text` - supports all **openai.client.audio.transcriptions.create** function params
> * `sqlalchemy` - supports all **SQLAlchemy.create_async_engine** function params

```toml
[security]
levels = [1, 2, 3]
zero = 0

[security.ai.textgen]
level = 1
allow_groups = true

[security.ai.textgen_inline]
level = 1
allow_groups = false

[security.ai.speech_to_text]
level = 2
allow_groups = true

[security.ai.imagegen]
level = 3
allow_groups = false

[sqlalchemy]
pool_pre_ping = false
echo = false

[locale]
languages = ["en", "uk"]

[locale.translator]
domain = "messages"
localedir = "locale"

[logger]
level = "DEBUG"

[openai]
directive = "Your name is Ayumi. You are a helpful telegram chat assistant. Act like a human. Respond in language you are asked."

[openai.text]
model = "gpt-4o-mini"

[openai.image]
size = "1024x1024"
model = "dall-e-3"

[openai.speech_to_text]
response_format = "text"
model = "whisper-1"

[inline.query]
min_len = 3
```


### See available `cli` commands

```shell
python main.py --help
```


### Recreate database schemas

> **Current version of Ayumi supports only async version of `SQLAlchemy` (tested only with `PostgreSQL` database and `asyncpg` driver).**

```shell
python main.py --reinit
```

### Compile locales [PyBabel guide](#pybabel-guide)

```shell
pybabel compile -d locale
```

### Start bot

```shell
python main.py
```


---


## Docker guide

### With remote `PostgreSQL` database

> Don't forget to set [required](#required-variables) variables in `Dockerfile` or directly in `docker run --env ...`

#### Build the image

```shell
docker build -t ayumi .
```

#### Create and start a container

```shell
docker run --env ... ayumi
```

### Docker compose `PostgreSQL + AyumiBot`

Create `.env` file in the project **root** and configure all [required](#required-variables) + [additional](#additional-variables) variables.

#### Build images and start containers

> The `ayumi_bot` container may restart several times, due to the long `postgres` container init

```shell
docker-compose up -d
```


---


## Telegram bot configuration via [BotFather](https://t.me/BotFather)

### How to highlight commands?

> Got to `@BOT_NAME > Edit Bot > Edit Commands` and send the following message

```text
start - Let's start <3
help - Usage guide
get_access - Ask for access to my AI features
users - The list of authorized users (admin only)
groups - The list of authorized groups (admin only)
```

### How to configure inline mode?

> Go to `@BOT_NAME > Bot Settings > Inline Mode` turn it on and set the placeholder

Example:
```text
Ask me anything
```


---


## Pybabel guide

### Extract keys

This command extracts all keys (values inside each `gettext` function) from sources

```shell
pybabel extract . -o locale/base.pot
```


### Init new locale

```shell
pybabel init -l de -i locale/base.pot -d locale
```

Once your new locale is created, you can edit it in `locale/de/LC_MESSAGES/messages.po`


### Update .po files

This command execution is required every time you **rename old or add new keys**

```shell
pybabel update -i locale/base.pot -d locale
```


### Compile locales

Once you have finished editing your locale, you must compile it `(otherwise, you'll see keys instead of actual translations)`

```shell
pybabel compile -d locale
```
