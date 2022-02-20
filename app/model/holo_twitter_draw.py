# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloTwitterDraw(Base):
    __tablename__ = 'holo_twitter_draw'

    twitter_id = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    twitter_user_nm = Column(String(100), nullable=False)
    twitter_user_id = Column(String(50), nullable=False)

    def __repr__(self):
        return "<HoloTwitterDraw(index='%s', twitter_id='%s', url='%s',twitter_user_nm='%s',twitter_user_id='%s')>" % (
            self.index,
            self.twitter_id,
            self.url,
            self.twitter_user_nm,
            self.twitter_user_id,
        )

    @classmethod
    def get_id(cls):
        return HoloTwitterDraw.index

    FIELDS = {"index": int, "twitter_id": str, "url": str, "twitter_user_nm": str, "twitter_user_id": str}

    FIELDS.update(Base.FIELDS)
