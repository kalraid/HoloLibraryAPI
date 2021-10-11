# -*- coding: utf-8 -*-
from builtins import print

from sqlalchemy import Column
from sqlalchemy import String, Integer

from app.config import UUID_LEN
from app.model import Base


class User(Base):
    user_id = Column(String(60), primary_key=True)
    username = Column(String(20), nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    access_token = Column(String(520), nullable=False)

    def __repr__(self):
        return "<User(name='%s', email='%s', access_token='%s')>" % (
            self.username,
            self.email,
            self.access_token,
        )

    @classmethod
    def get_id(cls):
        return User.user_id

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(User).filter(User.email == email).one()

    FIELDS = {"username": str, "email": str, "access_token": str}

    FIELDS.update(Base.FIELDS)