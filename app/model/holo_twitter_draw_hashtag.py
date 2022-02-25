# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from app.model import Base


# one tweet : N draw : M Tags  ->  N draw : M tags
class HoloTwitterDrawHashtag(Base):
    __tablename__ = 'holo_twitter_draw_hashtag'

    hashtag = Column(String(500), nullable=False)
    datatype = Column(String(30), nullable=False) # init, tweet, img
    tagtype = Column(String(30), nullable=False) # base, fanart, stream

    holo_twitter_draw_id = Column(Integer, ForeignKey('holo_twitter_draw.index'), nullable=True)
    holo_twitter_draw = relationship("HoloTwitterDraw", backref="holo_twitter_draw_hashtag")

    def __repr__(self):
        return "<HoloTwitterDrawHashtag(hashtag='%s', datatype='%s',tagtype='%s')>" % (
            self.hashtag,
            self.datatype,
            self.tagtype,
        )

    @classmethod
    def get_id(cls):
        return HoloTwitterDrawHashtag.index

    FIELDS = {"hashtag": str, "datatype": str, "tagtype": str}

    FIELDS.update(Base.FIELDS)
