"""This module contains translation keys and useful constants."""


from gettext import gettext
from dataclasses import dataclass

from ayumi.config import TELEGRAM_BOT_NAME, app_config


__all__ = (
    'ParseMode',
    'Command',
    'T',
    'Pattern',
    'Format',
    'ContentType'
)


# substring to use in `Pattern.access` to filter inline keyboards callback
SECURITY_LEVEL_FILTER = '|'.join([
    str(lvl)
    for lvl in app_config.security.levels + [app_config.security.zero]
])


@dataclass
class ParseMode:
    """pyTelegramBotAPI supported parse modes"""
    html: str = 'html'
    markdown: str = 'markdown'


@dataclass
class Command:
    """Define commands here"""
    start: tuple = ('start', 's')
    help: tuple = ('help', 'h')
    request_access: tuple = ('request_access', 'r')
    users: tuple = ('users', 'r')


@dataclass
class T:
    """Define translations here."""

    @dataclass
    class Common:
        """Common messages"""
        help: str = gettext('common.help')
        access_request: str = gettext('common.access_request')
        processing: str = gettext('common.processing')
        user_profile: str = gettext('common.user_profile')
        inline_title: str = gettext('common.inline_title')

    @dataclass
    class Access:
        """Access state messages"""
        granted: str = gettext('access.granted')
        refused: str = gettext('access.refused')
        pending: str = gettext('access.pending')

    @dataclass
    class Error:
        """Error messages"""
        api: str = gettext('error.api')
        permissions: str = gettext('error.permissions')
        auth: str = gettext('error.auth')

    @dataclass
    class AccessKeyboard:
        """AccessKeyboard buttons"""
        highlighted: str = gettext('access_keyboard.highlighted')
        level: str = gettext('access_keyboard.level')
        deny: str = gettext('access_keyboard.deny')


@dataclass
class Pattern:
    """Define callback/message filters here"""
    access: str = fr'\d*:({SECURITY_LEVEL_FILTER})\Z'
    gen_image: str = fr'\A({TELEGRAM_BOT_NAME}@i).*'
    gen_text: str = fr'\A{TELEGRAM_BOT_NAME}[^@].*'
    gen_request: str = fr'\A{TELEGRAM_BOT_NAME}(@i)*\W*'


@dataclass
class Format:
    """Callback formats"""
    access: str = '{uuid}:{level}'


@dataclass
class ContentType:
    """Content types (currently using just 2 of them)"""
    text: str = 'text'
    voice: str = 'voice'
