# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary, DATE
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class HoloMemberTwitter(Base):
    id = Column(Integer, primary_key=True)
    member_name = Column(String(80), unique=True, nullable=False) ## == holo_member.name
    content = Column(JSON, nullable=False)
    date = Column(DATE, nullable=True)


    def __repr__(self):
        return "<HoloMemberTwitter(id='%s', member_name='%s', content='%s', date='%s')>" % (
            self.id,
            self.member_name,
            self.content,
            self.date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitter.id


    FIELDS = {"id": str, "member_name": str, "content": alchemy.passby, "date": DATE}

    FIELDS.update(Base.FIELDS)