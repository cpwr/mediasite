import sys
import logging

import trafaret as t
from trafaret_config import read_and_validate
from trafaret_config import ConfigError

log = logging.getLogger(__name__)

DB_ENV_TRAFARET = t.Dict({
    'dsn': t.String(),
    'timeout': t.Int(),
})

APP_ENV_TRAFARET = t.Dict({
    'host': t.String(),
    'port': t.String(),
    'debug': t.Bool(),
})

CONFIG_TRAFARET = t.Dict({
    'db': DB_ENV_TRAFARET,
    'app': APP_ENV_TRAFARET,
})


def parse_config(path):
    try:
        config = read_and_validate(path, CONFIG_TRAFARET)
    except ConfigError as e:
        for error_message in e.errors:
            log.error(str(error_message))
        sys.exit(1)
    return config