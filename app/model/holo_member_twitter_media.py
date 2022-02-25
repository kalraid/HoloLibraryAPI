# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.model import Base


class HoloMemberTwitterMedia(Base):
    __tablename__ = 'holo_member_twitter_media'

    holo_member_tweet_id = Column(String(200), ForeignKey('holo_member_tweet.tweet_id'))
    holo_member_tweet = relationship("HoloMemberTweet", backref="holo_member_twitter_media")

    media_type = Column(String(10), nullable=True)  # photo, youtube, retweet
    media_link = Column(String(300), nullable=True)

    def __repr__(self):
        return "<HoloMemberTwitter(media_type='%s', media_link='%s')>" % (
            self.media_type,
            self.media_link,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterMedia.index

    FIELDS = {"index": int, "holo_member_tweet_id": int, "media_type": str, "media_link": str}

    FIELDS.update(Base.FIELDS)
