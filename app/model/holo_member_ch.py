# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String

from app.model import Base


class HoloMemberCh(Base):
    __tablename__ = 'holo_member_channel'

    channel_id = Column(String(400), primary_key=True)
    channel_name = Column(String(200), unique=True, nullable=False)
    channel_url = Column(String(400), unique=True, nullable=False)
    member_name = Column(String(80), nullable=False)  ## == holo_member.name
    company_name = Column(String(200), nullable=False)  ## == holo_company.name

    def __repr__(self):
        return "<HoloMemberCh(channel_id='%s', channel_name='%s', member_name='%s', channel_url='%s')>" % (
            self.channel_id,
            self.channel_name,
            self.member_name,
            self.channel_url,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberCh.user_id

    @classmethod
    def get_ids(cls, session):
        return session.query(HoloMemberCh.channel_id).all()

    @classmethod
    def get_ids(cls, session, company):
        return session.query(HoloMemberCh.channel_id).filter(HoloMemberCh.company_name == company).all()

    FIELDS = {"channel_id": str, "channel_name": str, "member_name": str, "company_name": str, "channel_url": str}

    FIELDS.update(Base.FIELDS)