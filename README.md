# Ayumi - AI-powered chat assistant
* Author: [satojkee](https://github.com/satojkee/)
* Project version: [ayumi-bot](https://github.com/satojkee/ayumi-bot/tree/v2)

## Usage guide

### Clone repository
```shell
git clone https://github.com/satojkee/ayumi-bot.git -b v2
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
| `OPENAI_MODEL_INSTRUCTIONS` | OpenAI model directive     |
| `OPENAI_IMAGE_MODEL`        | OpenAI default image model |
| `OPENAI_TEXT_MODEL`         | OpenAI default text model  |


### Edit `app_config.toml` if needed
```toml
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

[openai.image]
size = "1024x1024"

```
### Init database schemas
```shell
python main.py --init
```

### Start bot
```shell
python main.py
```

## Pybabel guide
> Create a new folder where the translation will be stored
```shell
mkdir locale
```

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