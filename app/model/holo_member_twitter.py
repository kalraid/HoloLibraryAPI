# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloMemberTwitter(Base):
    __tablename__ = 'holo_member_twitter'

    holo_member_twitter_info_id = Column(Integer, ForeignKey('holo_member_twitter_info.index'))
    holo_member_twitter_info = relationship("HoloMemberTwitterInfo", backref="holo_member_twitter")

    content = Column(JSON, nullable=False)
    date = Column(DATE, nullable=True)

    def __repr__(self):
        return "<HoloMemberTwitter(content='%s', date='%s')>" % (
            self.content,
            self.date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitter.index

    FIELDS = {"content": alchemy.passby, "date": DATE}

    FIELDS.update(Base.FIELDS)
