# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloMemberTwitterUrl(Base):
    __tablename__ = 'holo_member_twitter_url'

    holo_member_tweet_id = Column(String(50), ForeignKey('holo_member_tweet.tweet_id'))
    holo_member_tweet = relationship("HoloMemberTweet", backref="holo_member_twitter_url")

    url = Column(String(300), nullable=True)

    def __repr__(self):
        return "<HoloMemberTwitterUrl(url='%s')>" % (
            self.url
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterUrl.index

    FIELDS = {"url": String}

    FIELDS.update(Base.FIELDS)
