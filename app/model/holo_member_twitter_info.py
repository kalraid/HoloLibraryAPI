# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

import log
from app.model import Base

LOG = log.get_logger()
class HoloMemberTwitterInfo(Base):
    __tablename__ = 'holo_member_twitter_info'

    member_id = Column(Integer, ForeignKey('holo_member.index'))
    member = relationship("HoloMember", backref="holo_member_twitter_info")

    twitter_id = Column(String(50), primary_key=True, unique=True)
    twitter_username = Column(String(200), nullable=False)
    twitter_name = Column(String(500), nullable=False)
    twitter_url = Column(String(200), nullable=False)

    def __repr__(self):
        return "<HoloMemberTwitterInfo(index='%s', twitter_username='%s', twitter_name='%s', twitter_id='%s', twitter_url='%s')>" % (
            self.index,
            self.twitter_username,
            self.twitter_name,
            self.twitter_id,
            self.twitter_url,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterInfo.index

    @classmethod
    def find_by_twitter_info_id(cls, session, twitter_id):
        return session.query(HoloMemberTwitterInfo).filter(HoloMemberTwitterInfo.twitter_id == twitter_id).first()

    @classmethod
    def get_twitter_ids(cls, session):
        twitter_info_list = session.query(HoloMemberTwitterInfo.twitter_id).all()
        LOG.info("len list : {}".format(len(twitter_info_list)))
        return list(map(lambda i: i[0].strip(), twitter_info_list))

    FIELDS = {"index": str, "twitter_username": str, "twitter_name": str, "twitter_id": str, "twitter_url": str}

    FIELDS.update(Base.FIELDS)
