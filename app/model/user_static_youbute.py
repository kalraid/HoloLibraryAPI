# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer, DATE

from app.model import Base


class UserStaticYoutube(Base):
    __name__ == 'user_static_youtube'

    user_id = Column(String(60), primary_key=True)
    channel_id = Column(Integer, nullable=False, unique=True)
    member_name = Column(String(80), nullable=False)
    sub_date = Column(DATE, nullable=True)

    def __repr__(self):
        return "<UserStaticYoutube(user_id='%s', channel_id,='%s' member_name='%s', sub_date='%s')>" % (
            self.user_id,
            self.channel_id,
            self.member_name,
            self.sub_date,
        )

    @classmethod
    def get_id(cls):
        return UserStaticYoutube.user_id

    @classmethod
    def finds_static(cls, session, user_id):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).all()

    @classmethod
    def finds_static(cls, session, user_id, member_name):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).\
            filter(UserStaticYoutube.member_name == member_name).all()

    @classmethod
    def finds_first(cls, session, user_id, member_name):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).\
            filter(UserStaticYoutube.member_name == member_name).order_by(UserStaticYoutube.sub_date).first()

    @classmethod
    def get_age(cls, session, user_id, member_name):
        return session.query(UserStaticYoutube).filter(UserStaticYoutube.user_id == user_id).\
            filter(UserStaticYoutube.member_name == member_name).one()

    FIELDS = {"user_id": str, "channel_id": str, "member_name": str, "sub_date": DATE}

    FIELDS.update(Base.FIELDS)