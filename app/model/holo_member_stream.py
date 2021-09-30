# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, DATE

from app.model import Base


class HoloMemberStream(Base):
    __name__ == 'holo_member_stream'

    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    member_name = Column(String(80), nullable=False)  ## == holo_member.name
    start_date = Column(DATE, nullable=True)
    end_date = Column(DATE, nullable=True)

    def __repr__(self):
        return "<HoloMemberStream(id='%s', name='%s', member_name='%s', start_date='%s', end_date='%s')>" % (
            self.id,
            self.name,
            self.member_name,
            self.start_date,
            self.end_date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberStream.id

    @classmethod
    def get_name(cls):
        return HoloMemberStream.name


    FIELDS = {"id": str, "email": str, "name": str, "start_date": DATE,"end_date": DATE }

    FIELDS.update(Base.FIELDS)