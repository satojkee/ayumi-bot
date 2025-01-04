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
    """Each command represents a list[str]."""
    start: list[str] = ['start', 's']
    help: list[str] = ['help', 'h']
    request_access: list[str] = ['request_access', 'r']
    status: list[str] = ['status', 's']


class T:
    """Contains `pybabel` translated responses."""
    class Common:
        start: str = gettext('common.start')
        help: str = gettext('common.help')
        access_request: str = gettext('common.access_request')
        processing: str = gettext('common.processing')
        access_granted: str = gettext('common.access_granted')
        access_refused: str = gettext('common.access_refused')
        request_pending: str = gettext('common.request_pending')

    class Status:
        positive: str = gettext('status.positive')
        negative: str = gettext('status.negative')

    class ADKeyboard:
        approve: str = gettext('adk.approve')
        deny: str = gettext('adk.deny')
        revoke: str = gettext('adk.revoke')

    class Error:
        api: str = gettext('error.api')
        access: str = gettext('error.access')


class Pattern:
    access: str = r'\d*:(0|1)\Z'
    gen_image: str = fr'\A({TELEGRAM_BOT_NAME}@i).*'
    gen_text: str = fr'\A{TELEGRAM_BOT_NAME}[^@].*'
    gen_request: str = fr'\A{TELEGRAM_BOT_NAME}(@i)*\W*'


class Format:
    access: str = '{uuid}:{state}'


class ContentType:
    text: str = 'text'
