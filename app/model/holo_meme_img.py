# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, ForeignKey

from app.model import Base


class HoloMemeImg(Base):
    __tablename__ = 'holo_neme_img'

    meme_id = Column(Integer, ForeignKey('holo_neme.id'))
    file_name = Column(String)
    file_url = Column(String)

    def __repr__(self):
        return "<HoloMemeImg(meme_id='%s', file_name='%s', file_url='%s')>" % (
            self.meme_id,
            self.file_name,
            self.file_url,
        )

    @classmethod
    def get_id(cls):
        return HoloMemeImg.file_name

    FIELDS = {"meme_id": int, "file_name": str, "file_url": str}

    FIELDS.update(Base.FIELDS)
