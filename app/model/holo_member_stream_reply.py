# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary, DATE
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class HoloMemberStreamReply(Base):
    id = Column(Integer, primary_key=True)
    stream_id = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)
    reply_user = Column(String(80), nullable=False)
    date = Column(DATE, nullable=True)

    def __repr__(self):
        return "<HoloMemberStreamReply(id='%s', stream_id='%s', content='%s', reply_user='%s', date='%s')>" % (
            self.id,
            self.stream_id,
            self.content,
            self.date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberStreamReply.id

    FIELDS = {"id": str, "stream_id": str, "content": alchemy.passby, "reply_user": str, "date":DATE}

    FIELDS.update(Base.FIELDS)