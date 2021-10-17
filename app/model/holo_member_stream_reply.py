# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.utils import alchemy


class HoloMemberStreamReply(Base):
    __tablename__ = 'holo_member_stream_reply'

    index = Column(Integer, primary_key=True)
    stream_id = Column(Integer, nullable=False)
    content = Column(JSON, nullable=False)
    reply_user = Column(String(80), nullable=False)
    date = Column(DATE, nullable=True)

    def __repr__(self):
        return "<HoloMemberStreamReply(index='%s', stream_id='%s', content='%s', reply_user='%s', date='%s')>" % (
            self.index,
            self.stream_id,
            self.content,
            self.date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberStreamReply.index

    FIELDS = {"id": str, "stream_id": str, "content": alchemy.passby, "reply_user": str, "date":DATE}

    FIELDS.update(Base.FIELDS)