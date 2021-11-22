# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.model import Base


class HoloMember(Base):
    __tablename__ = 'holo_member'

    company_name_alias = Column(String(80), nullable=False)
    member_classification = Column(String(80), nullable=False)
    member_generation = Column(String(80), nullable=False)
    member_name_kor = Column(String(80), nullable=False, primary_key=True)
    member_name_eng = Column(String(80), nullable=False, primary_key=True)
    member_name_jp = Column(String(80), nullable=False, primary_key=True)

    def __repr__(self):
        return "<HoloMember(company_name_alias='%s', member_classification='%s', member_generation='%s', member_name_kor='%s', member_name_eng='%s', member_name_jp='%s')>" % (
            self.company_name_alias,
            self.member_classification,
            self.member_generation,
            self.member_name_kor,
            self.member_name_eng,
            self.member_name_jp,
        )

    @classmethod
    def get_id(cls):
        return HoloMember.member_name_kor

    @classmethod
    def find_by_id(cls, session, member_name_kor):
        return session.query(HoloMember).filter(HoloMember.member_name_kor == member_name_kor).one()

    @classmethod
    def finds_by_company(cls, session, company_name_alias):
        return session.query(HoloMember).filter(HoloMember.company_name_alias == company_name_alias).all()

    FIELDS = {"company_name_alias": str, "member_classification": str, "member_generation": str, "member_name_kor": str,
              "member_name_eng": str, "member_name_jp": str}

    FIELDS.update(Base.FIELDS)
