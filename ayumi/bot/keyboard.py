from typing import Callable, Union

from telebot import types
from telebot.util import quick_markup

from ayumi.bot.props import Format, T


__all__ = (
    'ad_keyboard',
    'revoke_keyboard'
)


def ad_keyboard(uuid: Union[int, str],
                t: Callable) -> types.InlineKeyboardMarkup:
    """Approve/Deny access request inline keyboard constructor.

    :param uuid: Union[int, str] - user's telegram id
    :param t: Callable - translator
    :return: InlineKeyboardMarkup - ready-to-use keyboard
    """
    return quick_markup({
        t(k): dict(callback_data=Format.access.format(uuid=uuid, state=s))
        for k, s in [(T.ADKeyboard.approve, 1), (T.ADKeyboard.deny, 0)]
    })


def revoke_keyboard(uuid: Union[int, str],
                    t: Callable) -> types.InlineKeyboardMarkup:
    """Revoke access inline keyboard constructor.

    :param uuid: Union[int, str] - user's telegram id
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
