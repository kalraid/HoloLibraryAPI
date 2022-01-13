# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy

import log

LOG = log.get_logger()

# a member tweet's hashtag
class HoloMemberTwitterHashtag(Base):
    __tablename__ = 'holo_member_twitter_hashtag'

    hashtag = Column(String(500), nullable=False)
    datatype = Column(String(30), nullable=False) # init, tweet, img
    type = Column(String(30), nullable=False) # base, fanart, stream

    holo_member_tweet_id = Column(String(50), ForeignKey('holo_member_tweet.tweet_id'), nullable=False)
    holo_member_tweet = relationship("HoloMemberTweet", backref="holo_member_twitter_hashtag")

    def __repr__(self):
        return "<HoloMemberTwitterHashtag(hashtag='%s',datatype='%s',type='%s')>" % (
            self.hashtag,
            self.datatype,
            self.type
        )

    @classmethod
    def get_id(cls):
        return HoloMemberTwitterHashtag.index

    @classmethod
    def get_group_by_hashtag(cls, session):
        hashtags =  session.query(HoloMemberTwitterHashtag.hashtag).filter(HoloMemberTwitterHashtag.isUse == "Y").group_by(HoloMemberTwitterHashtag.hashtag).all()
        LOG.info("len list : {}".format(len(hashtags)))
        return list(map(lambda i: i[0].strip(), hashtags))

    @classmethod
    def get_group_by_hashtag_not_use(cls, session):
        hashtags =  session.query(HoloMemberTwitterHashtag.hashtag).filter(HoloMemberTwitterHashtag.isUse == "N").group_by(HoloMemberTwitterHashtag.hashtag).all()
        LOG.info("len list : {}".format(len(hashtags)))
        return list(map(lambda i: i[0].strip(), hashtags))




    FIELDS = {"hashtag": String, "datatype": String, "type": String}

    FIELDS.update(Base.FIELDS)