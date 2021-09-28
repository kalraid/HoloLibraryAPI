# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class HoloMemberCh(Base):
    channel_id = Column(String(400), primary_key=True)
    channel_name = Column(String(200), nullable=False, unique=True)
    member_name = Column(String(80), unique=True, nullable=False) ## == holo_member.name
    company_name = Column(String(200), unique=True, nullable=False) ## == holo_company.name

    def __repr__(self):
        return "<HoloMemberCh(channel_id='%s', channel_name='%s', member_name='%s')>" % (
            self.channel_id,
            self.channel_name,
            self.member_name,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberCh.user_id

    @classmethod
    def get_ids(cls, session):
        return session.query(HoloMemberCh.channel_id).list()

    @classmethod
    def get_ids(cls, session, company):
        return session.query(HoloMemberCh.channel_id).filter(HoloMemberCh.company_name == company).list()

    FIELDS = {"channel_id": str, "channel_name": str, "member_name": str, "company_name": str}

    FIELDS.update(Base.FIELDS)