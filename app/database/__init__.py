# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.module.google_api.drive import getinitdatasheet

import log
from app import config

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

    from app.model import Base

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    __init_data__()


def __init_data__():
    from app.model.holo_member_ch import HoloMemberCh

    db_session.query(HoloMemberCh).count()
    df = getinitdatasheet()

    for index, data_row in df.iterrows():
        holoMemberCh = HoloMemberCh()

        index = data_row[1]
        contry_type = data_row[2]
        ordinal_type = data_row[3]

        holoMemberCh.company_name = data_row[0]
        holoMemberCh.member_name = data_row[3]
        holoMemberCh.channel_name = data_row[4]
        holoMemberCh.channel_id = data_row[5]
        holoMemberCh.channel_url = data_row[6]

        item = db_session.query(HoloMemberCh).filter(HoloMemberCh.channel_id == holoMemberCh.channel_id).first()
        if item is None:
            db_session.add(holoMemberCh)

    db_session.commit()