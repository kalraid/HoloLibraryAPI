# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, ARRAY
from sqlalchemy.orm import relationship

from app.model import Base


class HoloMeme(Base):
    __tablename__ = 'holo_meme'

    member_name = Column(ARRAY(String(80)), nullable=False)
    meme_name = Column(String(80), nullable=False)
    meme_describe = Column(String(500), nullable=False)
    meme_img = relationship("HoloMemeImg", backref="holo_neme_img")
    meme_stream = relationship("HoloMemeStream", backref="holo_neme_origin_stream")

    def __repr__(self):
        return "<HoloMeme(member_name='%s', meme_name='%s', meme_describe='%s')>" % (
            self.member_name,
            self.meme_name,
            self.meme_describe,
        )

    @classmethod
    def get_id(cls):
        return HoloMeme.meme_name

    FIELDS = {"meme_name": str, "member_name": str, "meme_describe": str}

    FIELDS.update(Base.FIELDS)
