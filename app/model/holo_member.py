# -*- coding: utf-8 -*-
from math import comb

from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class HoloMember(Base):
    fullname = Column(String(300), nullable=False, primary_key=True)
    name = Column(String(80), nullable=False)
    alias = Column(JSON, nullable=True) # TODO need to divde table
    company = Column(String(200), nullable=False)

    def __repr__(self):
        return "<HoloMember(member_name='%s', member_fullname='%s', member_alias='%s', member_company='%s')>" % (
            self.name,
            self.fullname,
            self.alias,
            self.company,
        )

    @classmethod
    def get_id(cls):
        return HoloMember.name

    @classmethod
    def find_by_id(cls, session, name):
        return session.query(HoloMember).filter(HoloMember.name == name).one()

    @classmethod
    def finds_by_company(cls, session, company):
        return session.query(HoloMember).filter(HoloMember.company == company).list()

    FIELDS = {"name": str, "fullname": str, "alias": alchemy.passby, "company": str}

    FIELDS.update(Base.FIELDS)