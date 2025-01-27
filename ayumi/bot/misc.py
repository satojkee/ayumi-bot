"""This module contains translation keys and useful constants."""


from dataclasses import dataclass

from ayumi.config import TELEGRAM_BOT_NAME, app_config


__all__ = (
    'ParseMode',
    'Command',
    'Pattern',
    'Format',
    'ContentType'
)


# substring to use in `Pattern.access` to filter inline keyboards callback
SECURITY_LEVEL_FILTER = '|'.join([
    str(lvl)
    for lvl in app_config.security.levels + [app_config.security.zero]
])


@dataclass(frozen=True)
class ParseMode:
    """pyTelegramBotAPI supported parse modes"""
    html: str = 'html'
    markdown: str = 'markdown'


@dataclass(frozen=True)
class Command:
    """Define commands here"""
    start: tuple = ('start', 's')
    help: tuple = ('help', 'h')
    get_access: tuple = ('get_access', 'r')
    users: tuple = ('users', 'u')
    groups: tuple = ('groups', 'g')


@dataclass(frozen=True)
class Pattern:
    """Define callback/message filters here"""
    access: str = fr'-?\d*:({SECURITY_LEVEL_FILTER})\Z'
    gen_image: str = fr'\A({TELEGRAM_BOT_NAME}@i).*'
    gen_text: str = fr'\A{TELEGRAM_BOT_NAME}[^@].*'
    gen_request: str = fr'\A{TELEGRAM_BOT_NAME}(@i)*\W*'


@dataclass(frozen=True)
class Format:
    """Callback formats"""
    access: str = '{chat_id}:{level}'


@dataclass(frozen=True)
class ContentType:
    """Content types (currently using just 2 of them)"""
    text: str = 'text'
    voice: str = 'voice'
