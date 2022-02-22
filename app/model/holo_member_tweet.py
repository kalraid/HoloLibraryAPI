# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Boolean, DATETIME
from sqlalchemy import String, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloMemberTweet(Base):
    __tablename__ = 'holo_member_tweet'

    tweet_id = Column(String(50), nullable=False, primary_key=True,unique=True) # id
    content = Column(String(1000), nullable=False) #text (but if text has String "https://t.co/???????", need to remove)
    date = Column(DATETIME, nullable=True) # created_at
    rt_tweet_id = Column(String(50), nullable=True) # RT id
    qt_tweet_id = Column(String(50), nullable=True) # QT id
    reply_tweet_id = Column(String(50), nullable=True) # REPLY id
    tweet_type = Column(String(20), nullable=False, default=None)
    is_holo_tweet = Column(Boolean, nullable=False, default=True)

    holo_member_twitter_info_id = Column(String(50), ForeignKey('holo_member_twitter_info.twitter_id'), nullable=True)
    holo_member_twitter_info = relationship("HoloMemberTwitterInfo", backref="holo_member_tweet")

    def __repr__(self):
        return "<HoloMemberTweet(index='%s', tweet_id='%s', content='%s', date='%s', rt_tweet_id='%s', qt_tweet_id='%s', tweet_type='%s')>" % (
            self.index,
            self.tweet_id,
            self.content,
            self.date,
            self.rt_tweet_id,
            self.qt_tweet_id,
            self.tweet_type
        )


    @classmethod
    def get_id(cls):
        return HoloMemberTweet.index

    @classmethod
    def find_by_twitter_id(cls, session, tweet_id):
        return session.query(HoloMemberTweet).filter(HoloMemberTweet.tweet_id == tweet_id).one()

    FIELDS = {"index": int, "tweet_id": str, "content": str, "date": str, "rt_tweet_id": str, "qt_tweet_id": str, "tweet_type": str}

    FIELDS.update(Base.FIELDS)
