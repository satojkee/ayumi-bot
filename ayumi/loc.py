from typing import Optional
from gettext import GNUTranslations, translation

from .config import app_config


__all__ = ('get_translator',)


# The list of supported locales in format: ["uk", ...]
supported_locales: list[str] = app_config.locales.supported
# The translation domain (messages)
translation_domain: str = app_config.locales.domain
# Locales location (./locale) dir
locales_dir: str = app_config.locales.path


def get_translator(
    lang: Optional[str] = None
) -> Optional[GNUTranslations.gettext]:
    """Use this function to get proper translator-func.
    ! Only supported languages `LOCALES` are supported !

    :param lang: str - language code, e.g: 'en' or 'en_US'
    :return: gettext - gettext function instance
    """
    if lang is None or lang not in supported_locales:
        lang = supported_locales[0]

    return translation(
        domain=translation_domain,
        localedir=locales_dir,
        languages=(lang,)
    ).gettext
