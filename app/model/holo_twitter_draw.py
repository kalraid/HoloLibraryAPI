# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloTwitterDraw(Base):
    __tablename__ = 'holo_twitter_draw'

    twitter_id = Column(String(200), nullable=True)
    url = Column(JSON, nullable=True)
    date = Column(DATE, nullable=True)

    holo_twitter_tag_id = Column(Integer, ForeignKey('holo_twitter_tag.index'))
    holo_twitter_tag = relationship("HoloTwitterTag", backref="holo_twitter_draw")

    def __repr__(self):
        return "<HoloTwitterDraw(twitter_id='%s', url='%s',date='%s')>" % (
            self.twitter_id,
            self.url,
            self.date,
        )

    @classmethod
    def get_id(cls):
        return HoloTwitterDraw.index


    FIELDS = {"content": alchemy.passby, "date": DATE}

    FIELDS.update(Base.FIELDS)