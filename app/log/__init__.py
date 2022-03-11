# -*- coding: utf-8 -*-

import logging
import sys

from app import config

logging.basicConfig(level=config.LOG_LEVEL)  # 해당 구문 적용 안됨, 그래서 logging 기본 레벨인 warn이 적용됨
logging.info('logging level setting : ',config.LOG_LEVEL)
LOG = logging.getLogger("API")
LOG.setLevel(config.LOG_LEVEL) # 따라서 LOGGER에만 따로 config 레벨을 적용
LOG.propagate = False

INFO_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s"
DEBUG_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S %z"

if config.APP_ENV == "live":
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler("/log/app.log", "a", 1 * 1024 * 1024, 10)
    formatter = logging.Formatter(INFO_FORMAT, TIMESTAMP_FORMAT)
    file_handler.setFormatter(formatter)
    LOG.addHandler(file_handler)

if config.APP_ENV == "dev" or config.APP_ENV == "local":
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(DEBUG_FORMAT, TIMESTAMP_FORMAT)
    stream_handler.setFormatter(formatter)
    LOG.addHandler(stream_handler)


def get_logger():
    return LOG