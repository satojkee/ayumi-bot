from gettext import gettext

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
slp = '|'.join([
    str(lvl)
    for lvl in app_config.security.levels + [app_config.security.zero]
])


class ParseMode:
    html: str = 'html'
    markdown: str = 'markdown'


class Command:
    """Define commands here"""
    start: list[str] = ['start', 's']
    help: list[str] = ['help', 'h']
    request_access: list[str] = ['request_access', 'r']
    users: list[str] = ['users', 'u']


class T:
    """Define translations here."""
    class Common:
        help: str = gettext('common.help')
        access_request: str = gettext('common.access_request')
        processing: str = gettext('common.processing')
        user_profile: str = gettext('common.user_profile')
        inline_title: str = gettext('common.inline_title')

    class Access:
        granted: str = gettext('access.granted')
        refused: str = gettext('access.refused')
        pending: str = gettext('access.pending')

    class Error:
        api: str = gettext('error.api')
        permissions: str = gettext('error.permissions')
        auth: str = gettext('error.auth')

    class AccessKeyboard:
        highlighted: str = gettext('access_keyboard.highlighted')
        level: str = gettext('access_keyboard.level')
        deny: str = gettext('access_keyboard.deny')


class Pattern:
    """Define patterns here."""
    access: str = fr'\d*:({slp})\Z'
    gen_image: str = fr'\A({TELEGRAM_BOT_NAME}@i).*'
    gen_text: str = fr'\A{TELEGRAM_BOT_NAME}[^@].*'
    gen_request: str = fr'\A{TELEGRAM_BOT_NAME}(@i)*\W*'


class Format:
    """Define formats here."""
    access: str = '{uuid}:{level}'


class ContentType:
    """Define content types here."""
    text: str = 'text'
    voice: str = 'voice'
