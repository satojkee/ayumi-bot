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
- Access management system ✔️
- Group chat support `coming soon`

<img alt="preview" src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExb282OXY5eHI2Z25kOXRzY2RneWI4amszeTV3cHY2anlqN3dib3FkdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VmfOoHbB3rzhHpvsRe/giphy.gif" />


## Useful links

* [OpenAI API docs](https://platform.openai.com/docs/overview)
* [pyTelegramBotAPI](https://pytba.readthedocs.io/en/latest/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [BotFather](https://telegram.me/BotFather)
* [GetIDsBot](https://t.me/getidsbot)


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

| Variable                  | Description             | Hint                                                                                                                        |
|---------------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `DATABASE_URI`            | Database credentials    | PostgreSQL + asyncpg, format: `postgresql+asyncpg://postgres:...`                                                           |
| `TELEGRAM_TOKEN`          | Telegram bot token      | visit [BotFather](https://t.me/BotFather) and create your own bot                                                           |
| `TELEGRAM_OWNER_ID`       | Telegram admin id       | use [GetIDsBot](https://t.me/getidsbot) to get your account id                                                              |
| `TELEGRAM_BOT_NAME`       | Telegram bot name       | this name is used as filter for prompts, e.g: `TELEGRAM_BOT_NAME, hello!` or `TELEGRAM_BOT_NAME@i, image of a cute kitten.` |
| `OPENAI_PROJECT_ID`       | OpenAI project ID       | visit [OpenAI](https://platform.openai.com/settings/organization/projects) and create a new project                         |
| `OPENAI_SECRET_KEY`       | OpenAI API token        | create a new `API-KEY` for a created project on OpenAI platform                                                             |



### Edit `app_config.toml` if needed
> For example, you can replace the `gpt-4o-mini` text-model with `gpt-3.5-turbo` or `gpt-4o`, **but don't forget to enable this model in your project settings on OpenAI platform**

```toml
[common]
temp = "temp"

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


### Init database schemas
> It's required to create necessary database schemas \
> **Current version of Ayumi supports only async version of `SQLAlchemy` (tested only with `PostgreSQL` database and `asyncpg` driver).**

```shell
python main.py --init
```


### Start bot
> Don't forget to configure `inline` mode for your bot with `setinline` command via [BotFather](https://t.me/BotFather) \
> **ONLY IF YOU WANT TO USE THIS FEATURE ^^**

```shell
python main.py
```


---


## Docker guide
> Don't forget to set required variables in `Dockerfile` or directly in `docker run --env ...`

### Build image

```shell
docker build -t ayumi .
```

### Create container
```shell
docker run --env ... ayumi
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
