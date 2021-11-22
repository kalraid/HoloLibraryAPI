# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloMemberTwitterDraw(Base):
    __tablename__ = 'holo_member_twitter_draw'

    content = Column(JSON, nullable=False)
    date = Column(DATE, nullable=True)

    holo_member_twitter_tag_id = Column(Integer, ForeignKey('holo_member_twitter_tag.index'))
    holo_member_twitter_tag = relationship("HoloMemberTwitterTag", backref="holo_member_twitter_draw")

    def __repr__(self):
        return "<HoloMemberTwitterDraw(content='%s', date='%s')>" % (
            self.content,
            self.date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterDraw.index


    FIELDS = {"content": alchemy.passby, "date": DATE}

    FIELDS.update(Base.FIELDS)