# Ayumi - AI-powered chat assistant

---

* Author: [satojkee](https://github.com/satojkee/)
* Project: [ayumi-bot](https://github.com/satojkee/ayumi-bot/)


## Useful links

* [OpenAI API docs](https://platform.openai.com/docs/overview)
* [pyTelegramBotAPI](https://pytba.readthedocs.io/en/latest/)
* [SQLAlchemy](https://www.sqlalchemy.org/)


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

| Variable                    | Description                |
|-----------------------------|----------------------------|
| `DATABASE_URI`              | Database credentials       |
| `TELEGRAM_TOKEN`            | Telegram bot token         |
| `TELEGRAM_OWNER_ID`         | Telegram admin id          |
| `TELEGRAM_OWNER_USERNAME`   | Telegram admin username    |
| `TELEGRAM_BOT_NAME`         | Telegram bot name          |
| `OPENAI_SECRET_KEY`         | OpenAI API token           |
| `OPENAI_PROJECT_ID`         | OpenAI project ID          |



### Edit `app_config.toml` if needed

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


### Init database schemas

```shell
python main.py --init
```


### Start bot
> Don't forget to configure `inline` mode for your bot with `setinline` command via [BotFather](https://t.me/BotFather) 

```shell
python main.py
```


## Docker guide

### Build image

```shell
docker build -t ayumi .
```

### Create container
> Don't forget to set required variables in `Dockerfile` or directly in `docker run --env ...`

```shell
docker run --env ... ayumi
```


## Pybabel guide

### Extract strings
> <b>PyBabel</b> automatically extracts all strings (values inside `gettext` function) from your sources

```shell
pybabel extract . -o locale/base.pot
```


### Init new locale

```shell
pybabel init -l en -i locale/base.pot -d locale
```


### Compile locales
> Compiles `messages.po` to `messages.mo` files

```shell
pybabel compile -d locale
```

### Update translations
> Always use this after string extraction

```shell
pybabel update -i locale/base.pot -d locale
```
