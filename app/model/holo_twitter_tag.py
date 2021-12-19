# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from app.model import Base


class HoloTwitterTag(Base):
    __tablename__ = 'holo_twitter_tag'

    name = Column(String(80), nullable=False)
    type = Column(String(80), nullable=False)  # live_tag, kirinuki_tag, fanart_tag, callab_tag, event_tag,
    relation_member_id = Column(String(50), nullable=True)

    def __repr__(self):
        return "<HoloTwitterTag(index='%s', name='%s', type='%s')>" % (
            self.index,
            self.name,
            self.type
        )

    @classmethod
    def get_id(cls):
        return HoloTwitterTag.index

    FIELDS = {"index": str, "name": str, "type": str}

    FIELDS.update(Base.FIELDS)
