# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer

from app.model import Base


class HoloMemberTwitterTag(Base):
    __tablename__ = 'holo_member_twitter_tag'


    index = Column(Integer, primary_key=True)
    member_name = Column(String(80), unique=True, nullable=False)  ## == holo_member.name
    name = Column(String(80), nullable=False)
    type = Column(String(80), nullable=False)

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