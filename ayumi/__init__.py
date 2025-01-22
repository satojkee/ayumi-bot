import logging

from .config import app_config


__all__ = (
    'logger',
    'start_ayumi',
    'init_schemas'
)


logger = logging.getLogger(__name__)

stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)

logger.setLevel(app_config.logger.level)
logger.addHandler(stderr_handler)


from .bot import *
from .db import *
