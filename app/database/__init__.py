# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import log
from app import config
from app.model import Base
from .init_holo_member import get_member_data
from .init_holo_member_ch import get_channel_data
from .init_holo_member_twitter import get_twitter_data

LOG = log.get_logger()


def get_engine(uri):
    LOG.info("Connecting to database..")
    options = {
        "pool_recycle": 3600,
        "pool_size": 10,
        "pool_timeout": 30,
        "max_overflow": 30,
        "echo": config.DB_ECHO,
        "execution_options": {"autocommit": config.DB_AUTOCOMMIT},
    }
    return create_engine(uri, **options)


db_session = scoped_session(sessionmaker())
engine = get_engine(config.DATABASE_URL)


def init_session():
    db_session.configure(bind=engine)

    #__init_table__()
    __init_data__()


def __init_table__():
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def __init_data__():
    get_member_data(db_session)
    get_channel_data(db_session)
    get_twitter_data(db_session)
