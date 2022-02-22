# -*- coding: utf-8 -*-
import configparser
import logging
import os

BRAND_NAME = "Falcon REST API Template"

SECRET_KEY = "xs4G5ZD9SwNME6nWRWrK_aq6Yb9H8VJpdwCzkTErFPw="
UUID_LEN = 10
UUID_ALPHABET = "".join(map(chr, range(48, 58)))
TOKEN_EXPIRES = 3600

APP_ENV = os.environ.get("APP_ENV") or "local"  # or 'live' to load live
INI_FILE = os.path.join(
    os.path.dirname(os.path.realpath('__file__')), "config/{}.ini".format(APP_ENV)
)

CONFIG = configparser.ConfigParser(interpolation=None)
CONFIG.read(INI_FILE)

MYSQL = CONFIG["mysql"]

DB_CONFIG = (
    MYSQL["user"],
    MYSQL["password"],
    MYSQL["host"],
    MYSQL["database"]
)
logging.error(DB_CONFIG)

DATABASE_URL = "mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4" % DB_CONFIG

DB_ECHO = True if CONFIG["database"]["echo"] == "yes" else False
DB_AUTOCOMMIT = True
logging.error(CONFIG["logging"]["level"])
LOG_LEVEL = CONFIG["logging"]["level"]
