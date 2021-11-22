# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy import String

from app.model import Base


class HoloMemeStream(Base):
    __tablename__ = 'holo_neme_stream'

    meme_id = Column(Integer, ForeignKey('holo_neme.id'))
    stream_name = Column(String)
    stream_url = Column(String)
    is_origin = Column(Boolean)

    def __repr__(self):
        return "<HoloMemeStream(meme_id='%s', stream_name='%s', stream_url='%s',is_origin='%s')>" % (
            self.meme_id,
            self.stream_name,
            self.stream_url,
            self.is_origin,
        )

    @classmethod
    def get_id(cls):
        return HoloMemeStream.stream_name

    FIELDS = {"meme_id": int, "stream_name": str, "stream_url": str, "is_origin": str }

    FIELDS.update(Base.FIELDS)
