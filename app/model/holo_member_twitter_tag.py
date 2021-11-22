# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship

from app.model import Base


class HoloMemberTwitterTag(Base):
    __tablename__ = 'holo_member_twitter_tag'

    name = Column(String(80), nullable=False)
    type = Column(String(80), nullable=False)

    holo_member_twitter_info_id = Column(Integer, ForeignKey('holo_member_twitter_info.index'))
    holo_member_twitter_info = relationship("HoloMemberTwitterInfo", backref="holo_member_twitter_tag")

    def __repr__(self):
        return "<HoloMemberTwitterDraw(index='%s', member_name='%s', name='%s', type='%s')>" % (
            self.index,
            self.member_name,
            self.name,
            self.type,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterTag.index


    FIELDS = {"index": str, "member_name": str, "name": str, "type": str}

    FIELDS.update(Base.FIELDS)