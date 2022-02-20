# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

from app.model import Base


class HoloMemberImage(Base):
    __tablename__ = 'holo_member_image'

    member_id = Column(Integer, ForeignKey('holo_member.index'))
    member = relationship("HoloMember", backref="holo_member_image")

    img_url = Column(String(300), nullable=False)
    img_type = Column(String(10), nullable=False) # small, circle, large

    def __repr__(self):
        return "<HoloMemberImage(index='%s',member_id='%s', img_url='%s', img_type='%s')>" % (
            self.index,
            self.member_id,
            self.img_url,
            self.img_type
        )

    @classmethod
    def get_id(cls):
        return HoloMemberImage.index

    @classmethod
    def find_by_all_var(cls, session) -> bool:
        # return session.query(HoloMemberImage).filter(HoloMemberImage.member_id == id).filter(HoloMemberImage.img_url == url).filter(HoloMemberImage.img_type == type)
        return exists().query(HoloMemberImage).filter(HoloMemberImage.member_id == cls.member_id).filter(HoloMemberImage.img_url == cls.img_url).filter(HoloMemberImage.img_type == cls.img_type)

    FIELDS = {"index": int, "member_id": int, "img_url": str, "img_type": str}

    FIELDS.update(Base.FIELDS)
