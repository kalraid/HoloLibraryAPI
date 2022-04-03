# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, scoped_session

import log
from app import config
from app.model import Base
from .init_holo_member import get_member_data
from .init_holo_member_ch import get_channel_data
from .init_holo_member_img import get_member_img_data
from .init_holo_member_twitter import get_twitter_data
from .init_holo_member_twitter_tags import get_twitter_tags_data
from .init_youtube_banner import get_youtube_banner
from .init_youtube_stream_list import get_youtube_data
from .init_twitter_banner import get_twitter_banner

LOG = log.get_logger()


def get_engine(uri):
    LOG.info("Connecting to database..")
    options = {
        "pool_recycle": 3600,
        "pool_size": 30,
        "pool_timeout": 30,
        "max_overflow": 70,
        "echo": config.DB_ECHO,
        "execution_options": {"autocommit": config.DB_AUTOCOMMIT},
    }
    return create_engine(uri, **options)


db_session = scoped_session(sessionmaker())
engine = get_engine(config.DATABASE_URL)


def get_session():
    return db_session


def init_session():
    db_session.configure(bind=engine)

    __init_table__()
    init_data()


def __init_table__():

    #drop_all(engine)
    create_all(engine)


def init_data():
    get_member_data(db_session)
    get_channel_data(db_session)
    get_member_img_data(db_session)
    get_twitter_data(db_session)
    get_twitter_tags_data(db_session)
    get_twitter_banner(db_session)
    get_youtube_banner(db_session)
    get_youtube_data(db_session)

def drop_all(engine):
    metadata = Base.metadata
    engine_name = engine.name
    foreign_key_turn_off = {
        'mysql': 'SET FOREIGN_KEY_CHECKS=0;',
        'postgresql': 'SET CONSTRAINTS ALL DEFERRED;',
        'sqlite': 'PRAGMA foreign_keys = OFF;',
    }
    foreign_key_turn_on = {
        'mysql': 'SET FOREIGN_KEY_CHECKS=1;',
        'postgresql': 'SET CONSTRAINTS ALL IMMEDIATE;',
        'sqlite': 'PRAGMA foreign_keys = ON;',
    }
    truncate_query = {
        'mysql': 'DROP TABLE IF EXISTS {};',
        'postgresql': 'TRUNCATE TABLE {} RESTART IDENTITY CASCADE;',
        'sqlite': 'DELETE FROM {};',
    }

    with engine.begin() as conn:
        conn.execute(foreign_key_turn_off[engine.name])

        for table in reversed(metadata.sorted_tables):
            try:
                conn.execute(truncate_query[engine.name].format(table.name))
            except ProgrammingError as error:
                print(error)
        conn.execute(foreign_key_turn_on[engine.name])


def create_all(engine):
    metadata = Base.metadata # 여러분의 Base를 가져오세요!
    engine_name = engine.name
    foreign_key_turn_off = {
        'mysql': 'SET FOREIGN_KEY_CHECKS=0;',
        'postgresql': 'SET CONSTRAINTS ALL DEFERRED;',
        'sqlite': 'PRAGMA foreign_keys = OFF;',
    }
    foreign_key_turn_on = {
        'mysql': 'SET FOREIGN_KEY_CHECKS=1;',
        'postgresql': 'SET CONSTRAINTS ALL IMMEDIATE;',
        'sqlite': 'PRAGMA foreign_keys = ON;',
    }
    with engine.begin() as conn:
        conn.execute(foreign_key_turn_off[engine.name])
        Base.metadata.create_all(engine)
        conn.execute(foreign_key_turn_on[engine.name])


