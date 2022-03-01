# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String

from app.model import Base


class HoloTwitterDraw(Base):
    __tablename__ = 'holo_twitter_draw'

    twitter_id = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    twitter_user_nm = Column(String(100), nullable=False)
    twitter_user_id = Column(String(50), nullable=False)

    def __repr__(self):
        return "<HoloTwitterDraw(index='%s', twitter_id='%s', url='%s',twitter_user_nm='%s',twitter_user_id='%s',isUse='%s')>" % (
            self.index,
            self.twitter_id,
            self.url,
            self.twitter_user_nm,
            self.twitter_user_id,
            self.isUse,
        )

    @classmethod
    def get_id(cls):
        return HoloTwitterDraw.index

    @classmethod
    def get_by_id(cls, session, index):
        return session.query(HoloTwitterDraw).where(HoloTwitterDraw.index == index).one()

    FIELDS = {"index": int, "twitter_id": str, "url": str, "twitter_user_nm": str, "twitter_user_id": str, 'isUse': str}

    FIELDS.update(Base.FIELDS)
