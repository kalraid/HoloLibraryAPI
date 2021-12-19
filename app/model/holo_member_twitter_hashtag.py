# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloMemberTwitterHashtag(Base):
    __tablename__ = 'holo_member_twitter_hashtag'

    holo_member_tweet_id = Column(String(50), ForeignKey('holo_member_tweet.tweet_id'))
    holo_member_tweet = relationship("HoloMemberTweet", backref="holo_member_twitter_hashtag")

    hashtag = Column(String(100), nullable=True)

    def __repr__(self):
        return "<HoloMemberTwitterHashtag(hashtag='%s')>" % (
            self.hashtag
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterHashtag.index

    FIELDS = {"hashtag": String}

    FIELDS.update(Base.FIELDS)
