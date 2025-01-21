from typing import Callable

from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup

from ayumi.bot.props import Format, T


__all__ = (
    'ad_keyboard',
    'revoke_keyboard'
)


def ad_keyboard(uuid: int, t: Callable) -> InlineKeyboardMarkup:
    """Approve/Deny access request inline keyboard constructor.

    :param uuid: int - user's telegram id
    :param t: Callable - translator
    :return: InlineKeyboardMarkup - ready-to-use keyboard
    """
    return quick_markup({
        t(k): dict(callback_data=Format.access.format(uuid=uuid, state=s))
        for k, s in [(T.ADKeyboard.approve, 1), (T.ADKeyboard.deny, 0)]
    })


def revoke_keyboard(uuid: int, t: Callable) -> InlineKeyboardMarkup:
    """Revoke access inline keyboard constructor.

    :param uuid: int - user's telegram id
    :param t: Callable - translator
    :return: InlineKeyboardMarkup - ready-to-use keyboard
    """
    return quick_markup({
        t(T.ADKeyboard.revoke): dict(
            callback_data=Format.access.format(
                uuid=uuid,
                state=0
            )
        )
    })
