# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloMemberTwitterMention(Base):
    __tablename__ = 'holo_member_twitter_mention'

    holo_member_tweet_id = Column(String(200), ForeignKey('holo_member_tweet.tweet_id'))
    holo_member_tweet = relationship("HoloMemberTweet", backref="holo_member_twitter_mention")

    mention_user_id = Column(String(50), nullable=True)

    def __repr__(self):
        return "<HoloMemberTwitterMention(mention_user='%s')>" % (
            self.mention_user
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterMention.index

    FIELDS = {"mention_user": String}

    FIELDS.update(Base.FIELDS)
