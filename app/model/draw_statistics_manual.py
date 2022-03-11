# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from app.model import Base


class DrawStatisticsMenual(Base):
    __tablename__ = 'draw_statistics_menual'

    holo_twitter_draw_id = Column(Integer, ForeignKey('holo_twitter_draw.index'), nullable=True)
    holo_twitter_draw = relationship("HoloTwitterDraw", backref="draw_statistics_menual")

    holo_twitter_custom_draw_id = Column(Integer, ForeignKey('holo_twitter_custom_draw.index'), nullable=True)
    holo_twitter_custom_draw = relationship("HoloTwitterCustomDraw", backref="draw_statistics_menual")

    event = Column(String(10), nullable=False, index=True)  # like, dislike, ban, adult # one user one event
    like = Column(Integer, nullable=False, default=0)
    dislike = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<DrawStatisticsMenual(index='%s', holo_twitter_draw_id='%s', holo_twitter_custom_draw_id='%s',event='%s',like='%s',dislike='%s')>" % (
            self.index,
            self.holo_twitter_draw_id,
            self.holo_twitter_custom_draw_id,
            self.event,
            self.like,
            self.dislike
        )

    @classmethod
    def get_id(cls):
        return DrawStatisticsMenual.index

    @classmethod
    def save_count(cls, session, draw_id, img_type, event):

        if 'base' in img_type:
            cls.holo_twitter_draw_id = draw_id
            drawStaticsMenual = session.query(DrawStatisticsMenual) \
                .filter(DrawStatisticsMenual.holo_twitter_draw_id == draw_id) \
                .filter(DrawStatisticsMenual.event == event).first()
        elif 'custom' in img_type:
            cls.holo_twitter_custom_draw_id = draw_id
            drawStaticsMenual = session.query(DrawStatisticsMenual) \
                .filter(DrawStatisticsMenual.holo_twitter_custom_draw_id == draw_id) \
                .filter(DrawStatisticsMenual.event == event).first()

        if event == 'like': # like ++
            cls.like = 1
        elif event == 'dislike': # dislike ++
            cls.dislike = 1

        if drawStaticsMenual is None:
            cls.event = event
            session.add(cls)
        else:
            drawStaticsMenual.like += cls.like
            drawStaticsMenual.dislike += cls.dislike

    FIELDS = {"index": int, "holo_twitter_draw_id": str, "holo_twitter_custom_draw_id": str, "event": str,
              "like": int, "dislike": int}

    FIELDS.update(Base.FIELDS)
