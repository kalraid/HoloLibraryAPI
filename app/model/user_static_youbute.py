# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary, DATE
from sqlalchemy.dialects.mysql import JSON

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy


class UserStaticYoutube(Base):
    user_id = Column(Integer, primary_key=True)
    member_name = Column(String(80), nullable=False)
    sub_date = Column(DATE, nullable=True)


    def __repr__(self):
        return "<UserStaticYoutube(user_id='%s', member_name='%s', sub_date='%s')>" % (
            self.user_id,
            self.member_name,
            self.sub_date,
        )

    @classmethod
    def get_id(cls):
        return UserStaticYoutube.user_id

    @classmethod
    def finds_static(cls, session, user_id):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).list()

    @classmethod
    def finds_static(cls, session, user_id, member_name):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).\
            filter(UserStaticYoutube.member_name == member_name).list()

    @classmethod
    def finds_first(cls, session, user_id, member_name):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).\
            filter(UserStaticYoutube.member_name == member_name).order_by(UserStaticYoutube.sub_date).first()

    @classmethod
    def get_age(cls, session, user_id, member_name):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).\
            filter(UserStaticYoutube.member_name == member_name).one()

    FIELDS = {"user_id": str, "member_name": str, "sub_date": DATE}

    FIELDS.update(Base.FIELDS)