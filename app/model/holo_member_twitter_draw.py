# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.utils import alchemy


class HoloMemberTwitterDraw(Base):
    __name__ == 'holo_member_twitter_draw'

    id = Column(Integer, primary_key=True)
    member_name = Column(String(80), unique=True, nullable=False)  ## == holo_member.name
    tag_id = Column(Integer, primary_key=True)
    content = Column(JSON, nullable=False)
    date = Column(DATE, nullable=True)

    def __repr__(self):
        return "<HoloMemberTwitterDraw(id='%s', member_name='%s', content='%s', date='%s')>" % (
            self.id,
            self.member_name,
            self.content,
            self.date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterDraw.id


    FIELDS = {"id": str, "member_name": str, "content": alchemy.passby, "date": DATE}

    FIELDS.update(Base.FIELDS)