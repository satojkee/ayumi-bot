# Ayumi - AI-powered chat assistant for telegram

[![BotPicture](https://i.imgur.com/dh6PRx9.png)](https://t.me/myAyumi_bot)

---

* Author: [satojkee](https://github.com/satojkee/)
* Project: [ayumi-bot](https://github.com/satojkee/ayumi-bot/)


## Features

- Text generation ✔️
- Image generation ✔️
- Speech-to-text ✔️
- Inline mode support ✔️
- Private chat support ✔️
- Access management system with different levels of access ✔️
- Group chat support `coming soon`

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


### Edit `app_config.toml` if needed
> For example, you can replace the `gpt-4o-mini` text-model with `gpt-3.5-turbo` or `gpt-4o`, **but don't forget to enable this model in your project settings on OpenAI platform**
> 
> ### Explanation
>
> * `security`
>   * **levels** - a list of supported security levels in ascending order
>   * **zero** - this value is used in **keyboard.access_keyboard** and **handlers.admin.access_callback** to represent negative access response
>
> * `security.ai` - define required security levels for AI features here
>   * **textgen** - security level to access text generation feature
>   * **textgen_inline** - security level to access text generation in inline mode
>   * **speech_to_text** - security level to access speech-to-text feature
>   * **imagegen** - security level to access image generation feature
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
> * `locale.translator` - supports all `gettext.translation` function params
> * `openai.text` - supports all **openai.client.chat.completion.create** function params
> * `openai.image` - supports all **openai.client.images.generate** function params
> * `openai.speech_to_text` - supports all **openai.client.audio.transcriptions.create** function params
> * `sqlalchemy` - supports all **SQLAlchemy.create_async_engine** function params

```toml
[security]
levels = [1, 2, 3]
zero = 0

[security.ai]
textgen = 1
textgen_inline = 1
speech_to_text = 2
imagegen = 3

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


### Start bot
> Don't forget to configure `inline` mode for your bot with `setinline` command via [BotFather](https://t.me/BotFather) \
> **ONLY IF YOU WANT TO USE THIS FEATURE ^^**

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

### Docker-compose `PostgreSQL + AyumiBot`
Create `.env` file in the project **root** and configure all [required](#required-variables) + [additional](#additional-variables) variables.

#### Build images and start containers
> The `ayumi_bot` container may restart several times, due to the long `postgres` container init

```shell
docker-compose up -d
```


---


## Pybabel guide

### Extract keys
> <b>PyBabel</b> automatically extracts all strings (values inside `gettext` function) from your sources

```shell
pybabel extract . -o locale/base.pot
```


### Init new locale

```shell
pybabel init -l en -i locale/base.pot -d locale
```


### Update .po files
> Always use this after `extraction`

```shell
pybabel update -i locale/base.pot -d locale
```


### Compile locales
> Compiles `messages.po` to `messages.mo` files

```shell
pybabel compile -d locale
```
