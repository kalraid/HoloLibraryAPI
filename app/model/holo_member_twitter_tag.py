# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary, DATE
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class HoloMemberTwitterTag(Base):
    id = Column(Integer, primary_key=True)
    member_name = Column(String(80), unique=True, nullable=False) ## == holo_member.name
    name = Column(String(80), nullable=False)
    type = Column(String(80), nullable=False)

    def __repr__(self):
        return "<HoloMemberTwitterDraw(id='%s', member_name='%s', name='%s', type='%s')>" % (
            self.id,
            self.member_name,
            self.name,
            self.type,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterTag.id


    FIELDS = {"id": str, "member_name": str, "name": str, "type": str}

    FIELDS.update(Base.FIELDS)