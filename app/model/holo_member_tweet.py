# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Boolean, DATETIME
from sqlalchemy import String, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy


class HoloMemberTweet(Base):
    __tablename__ = 'holo_member_tweet'

    tweet_id = Column(String(200), nullable=False, primary_key=True,unique=True) # id
    content = Column(String(1000), nullable=False) #text (but if text has String "https://t.co/???????", need to remove)
    date = Column(DATETIME, nullable=True) # created_at
    rt_tweet_id = Column(String(200), nullable=True) # RT id
    qt_tweet_id = Column(String(200), nullable=True) # QT id
    reply_tweet_id = Column(String(200), nullable=True) # REPLY id
    type = Column(String(20), nullable=False, default=None)
    is_holo_tweet = Column(Boolean, nullable=False, default=True)
    hashtags = Column(JSON, nullable=True)
    urls = Column(JSON, nullable=True)
    user_mentions = Column(JSON, nullable=True)
    media = Column(JSON, nullable=True)

    holo_member_twitter_info_id = Column(String(50), ForeignKey('holo_member_twitter_info.twitter_id'), nullable=True)
    holo_member_twitter_info = relationship("HoloMemberTwitterInfo", backref="holo_member_tweet")

    def __repr__(self):
        return "<HoloMemberTweet(index='%s', tweet_id='%s', content='%s', date='%s', rt_tweet_id='%s', qt_tweet_id='%s', type='%s', is_holo_tweet='%s', hashtags='%s', urls='%s', user_mentions='%s', media='%s')>" % (
            self.index,
            self.tweet_id,
            self.content,
            self.date,
            self.rt_tweet_id,
            self.qt_tweet_id,
            self.type,
            self.is_holo_tweet,
            self.hashtags,
            self.urls,
            self.user_mentions,
            self.media,
        )


    @classmethod
    def get_id(cls):
        return HoloMemberTweet.index

    @classmethod
    def find_by_twitter_id(cls, session, tweet_id):
        return session.query(HoloMemberTweet).filter(HoloMemberTweet.tweet_id == tweet_id).one()

    FIELDS = {"content": alchemy.passby, "tweet_id": str, "date": DATETIME, "rt_tweet_id": str, "qt_tweet_id": str, "type": str, "is_holo_tweet": str, "hashtags": str, "urls": str, "user_mentions": str, "media": str}

    FIELDS.update(Base.FIELDS)
