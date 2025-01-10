from typing import Optional, Callable
from gettext import translation

from .config import app_config


__all__ = ('get_translator',)


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
