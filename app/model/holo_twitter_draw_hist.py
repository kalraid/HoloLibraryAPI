# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloTwitterDrawHist(Base):
    __tablename__ = 'holo_twitter_draw_hist'

    user_id = Column(String(60), ForeignKey('user.user_id'), nullable=True) # can be null
    user = relationship("User", backref="holo_twitter_draw_hist")

    holo_twitter_draw_id = Column(Integer, ForeignKey('holo_twitter_draw.index'), nullable=True)
    holo_twitter_draw = relationship("HoloTwitterDraw", backref="holo_twitter_draw_hist")

    holo_twitter_custom_draw_id = Column(Integer, ForeignKey('holo_twitter_custom_draw.index'), nullable=True)
    holo_twitter_custom_draw = relationship("HoloTwitterCustomDraw", backref="holo_twitter_draw_hist")

    event_type = Column(String(10), nullable=False) # click, download,

    def __repr__(self):
        return "<HoloTwitterDraw(twitter_id='%s', url='%s',twitter_user_nm='%s',twitter_user_id='%s')>" % (
            self.twitter_id,
            self.url,
            self.twitter_user_nm,
            self.twitter_user_id,
        )

    @classmethod
    def get_id(cls):
        return HoloTwitterDraw.index

    FIELDS = {"twitter_id": str, "url": str, "twitter_user_nm": str, "twitter_user_id": str}

    FIELDS.update(Base.FIELDS)
