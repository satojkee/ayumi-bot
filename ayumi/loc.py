"""This module contains a translation related functions."""


from dataclasses import dataclass
from typing import Optional, Callable
from gettext import translation, gettext

from .config import app_config


__all__ = ('get_translator', 'T')


def get_translator(lang: Optional[str] = None) -> Callable:
    """Use this function to get proper translator-func.
    ! Only supported languages `LOCALES` are supported !

    :param lang: str - language code, e.g: 'en' or 'en_US'
    :return: gettext - gettext function instance
    """
    if lang is None or lang not in app_config.locale.languages:
        lang = app_config.locale.languages[0]

    return translation(**app_config.locale.translator,
                       languages=(lang,)).gettext


@dataclass
class T:
    """Define translations here."""

    @dataclass
    class Common:
        """Common messages"""
        help: str = gettext('common.help')
        access_request: str = gettext('common.access_request')
        processing: str = gettext('common.processing')
        chat_profile: str = gettext('common.chat_profile')
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
