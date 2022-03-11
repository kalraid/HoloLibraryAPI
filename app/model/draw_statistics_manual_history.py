# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from app.model import Base


class DrawStatisticsMenualHistory(Base):
    __tablename__ = 'draw_statistics_menual_history'

    holo_twitter_draw_id = Column(Integer, ForeignKey('holo_twitter_draw.index'), nullable=True)
    holo_twitter_draw = relationship("HoloTwitterDraw", backref="draw_statistics_menual_history")

    holo_twitter_custom_draw_id = Column(Integer, ForeignKey('holo_twitter_custom_draw.index'), nullable=True)
    holo_twitter_custom_draw = relationship("HoloTwitterCustomDraw", backref="draw_statistics_menual_history")

    event = Column(String(10), nullable=False, index=True)  # like, dislike, ban, adult # one user one event
    user_uuid = Column(String(40), nullable=False)

    def __repr__(self):
        return "<DrawStatisticsMenualHistory(index='%s', holo_twitter_draw_id='%s', holo_twitter_custom_draw_id='%s',event='%s',user_uuid='%s')>" % (
            self.index,
            self.holo_twitter_draw_id,
            self.holo_twitter_custom_draw_id,
            self.event,
            self.user_uuid,
        )

    @classmethod
    def get_id(cls):
        return DrawStatisticsMenualHistory.index

    @classmethod
    def get_manual_event_names(cls):
        return ['like', 'dislike', 'ban', 'adult']

    @classmethod
    def get_manual_adult_event_names(cls):
        return [ 'ban', 'adult']

    FIELDS = {"index": int, "holo_twitter_draw_id": str, "holo_twitter_custom_draw_id": str, "event": str,
              "user_uuid": str}

    FIELDS.update(Base.FIELDS)
