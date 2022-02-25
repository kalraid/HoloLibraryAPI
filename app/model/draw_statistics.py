# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from app.model import Base


class DrawStatistics(Base):
    __tablename__ = 'draw_statistics'

    holo_twitter_draw_id = Column(Integer, ForeignKey('holo_twitter_draw.index'), nullable=True)
    holo_twitter_draw = relationship("HoloTwitterDraw", backref="draw_statistics")

    holo_twitter_custom_draw_id = Column(Integer, ForeignKey('holo_twitter_custom_draw.index'), nullable=True)
    holo_twitter_custom_draw = relationship("HoloTwitterCustomDraw", backref="draw_statistics")

    event = Column(String(10), nullable=False)
    user_uuid = Column(String(40), nullable=False)

    def __repr__(self):
        return "<DrawStatistics(index='%s', holo_twitter_draw_id='%s', holo_twitter_custom_draw_id='%s',event='%s',user_uuid='%s')>" % (
            self.index,
            self.holo_twitter_draw_id,
            self.holo_twitter_custom_draw_id,
            self.event,
            self.user_uuid,
        )

    @classmethod
    def get_id(cls):
        return DrawStatistics.index

    FIELDS = {"index": int, "holo_twitter_draw_id": str, "holo_twitter_custom_draw_id": str, "event": str,
              "user_uuid": str}

    FIELDS.update(Base.FIELDS)
