"""This module contains functions that construct telegram keyboards."""


from typing import Callable, Union, Optional

from telebot import types
from telebot.util import quick_markup

from ayumi.bot.props import Format, T
from ayumi.config import app_config


__all__ = ('access_keyboard',)


def access_keyboard(
    uuid: Union[int, str],
    t: Callable,
    highlight: Optional[int] = None
) -> types.InlineKeyboardMarkup:
    """Access management system as inline keyboard.

    :param uuid: Union[int, str] - user's telegram id
    :param t: Callable - translator
    :param highlight: Optional[int] - level to highlight
    :return: InlineKeyboardMarkup - ready-to-use keyboard
    """
    layout = {}
    for level in app_config.security.levels:
        if level == highlight:
            key = T.AccessKeyboard.highlighted
        else:
            key = T.AccessKeyboard.level
        # add button to the layout
        layout.setdefault(
            t(key).format(value=level),
            {'callback_data': Format.access.format(uuid=uuid, level=level)}
        )

    # additional `Deny` button, that should be the last one
    layout.setdefault(
        t(T.AccessKeyboard.deny),
        {
            'callback_data': Format.access.format(
                uuid=uuid,
                level=app_config.security.zero
            )
        }
    )

    return quick_markup(layout, row_width=3)
