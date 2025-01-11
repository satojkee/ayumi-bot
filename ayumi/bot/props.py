from gettext import gettext

from ayumi.config import TELEGRAM_BOT_NAME


__all__ = (
    'ParseMode',
    'Command',
    'T',
    'Pattern',
    'Format',
    'ContentType'
)


class ParseMode:
    html: str = 'html'
    markdown: str = 'markdown'


class Command:
    """Define commands here"""
    start: list[str] = ['start', 's']
    help: list[str] = ['help', 'h']
    request_access: list[str] = ['request_access', 'r']
    users: list[str] = ['users', 'u']
    status: list[str] = ['status', 's']


class T:
    """Define translations here."""
    class Common:
        start: str = gettext('common.start')
        help: str = gettext('common.help')
        access_request: str = gettext('common.access_request')
        processing: str = gettext('common.processing')
        user_profile: str = gettext('common.user_profile')

    class Access:
        granted: str = gettext('access.granted')
        refused: str = gettext('access.refused')
        pending: str = gettext('access.pending')

    class ADKeyboard:
        approve: str = gettext('adk.approve')
        deny: str = gettext('adk.deny')
        revoke: str = gettext('adk.revoke')

    class Error:
        api: str = gettext('error.api')
        permissions: str = gettext('error.permissions')


class Pattern:
    """Define patterns here."""
    access: str = r'\d*:(0|1)\Z'
    gen_image: str = fr'\A({TELEGRAM_BOT_NAME}@i).*'
    gen_text: str = fr'\A{TELEGRAM_BOT_NAME}[^@].*'
    gen_request: str = fr'\A{TELEGRAM_BOT_NAME}(@i)*\W*'


class Format:
    """Define formats here."""
    access: str = '{uuid}:{state}'


class ContentType:
    """Define content types here."""
    text: str = 'text'
    voice: str = 'voice'
