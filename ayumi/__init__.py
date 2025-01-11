import os
import json
import logging

from .config import app_config


__all__ = (
    'logger',
    'start_ayumi',
    'init_schemas'
)


# create temp dir if not exists
if not os.path.exists(app_config.common.temp):
    os.mkdir(app_config.common.temp)

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

# displays running configuration
logger.debug('starting ayumi')
logger.debug(f'running configuration: {json.dumps(app_config, indent=2)}')


from .bot import *
from .db import *
