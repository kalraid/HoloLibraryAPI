# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String

from app.model import Base


# SQLALchmy 관련링크
## https://edykim.com/ko/post/getting-started-with-sqlalchemy-part-1/
## https://lowelllll.github.io/til/2019/04/19/TIL-flask-sqlalchemy-orm/
## https://blog.hongminhee.org/2013/10/30/65522658529/

class HoloCompany(Base):
    __name__ == 'holo_company'

    name = Column(String(200), primary_key=True)

    def __repr__(self):
        return "<HoloCompany(name='%s')>" % (
            self.username
        )

    @classmethod
    def get_id(cls):
        return HoloCompany.name

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(HoloCompany).filter(HoloCompany.name == name).one()

    FIELDS = {"name": str}

    FIELDS.update(Base.FIELDS)