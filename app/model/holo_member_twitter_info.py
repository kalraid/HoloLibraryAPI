# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship, backref

from app.model import Base
from app.utils import alchemy


class HoloMemberTwitterInfo(Base):
    __tablename__ = 'holo_member_twitter_info'

    member_id = Column(Integer, ForeignKey('holo_member.index'))
    member = relationship("HoloMember", backref="holo_member_twitter_info")

    twitter_id = Column(String(50), primary_key=True)
    twitter_username = Column(String(200), nullable=False)
    twitter_name = Column(String(500), nullable=False)
    twitter_url = Column(String(200), nullable=False)

    def __repr__(self):
        return "<HoloMemberTwitter(index='%s', twitter_username='%s', twitter_name='%s', twitter_id='%s', twitter_url='%s')>" % (
            self.index,
            self.twitter_username,
            self.twitter_name,
            self.twitter_id,
            self.twitter_url,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterInfo.index

    FIELDS = {"index": str, "twitter_username": str, "twitter_name": str, "twitter_id": str, "twitter_url": str}

    FIELDS.update(Base.FIELDS)
