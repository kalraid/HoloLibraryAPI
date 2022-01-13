# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.model import Base
from app.utils import alchemy

import log

LOG = log.get_logger()

# main tag list
class HoloMemberHashtag(Base):
    __tablename__ = 'holo_member_hashtag'

    hashtag = Column(String(500), nullable=False)
    datatype = Column(String(30), nullable=False) # init, tweet, img
    type = Column(String(30), nullable=False) # base, fanart, stream

    member_id = Column(Integer, ForeignKey('holo_member.index'), nullable=True)
    member = relationship("HoloMember", backref="holo_member_hashtag")

    def __repr__(self):
        return "<holo_member_hashtag(hashtag='%s',datatype='%s',type='%s', member_id='%s')>" % (
            self.hashtag,
            self.datatype,
            self.type,
            self.member_id
        )

    @classmethod
    def get_id(cls):
        return HoloMemberHashtag.index

    @classmethod
    def get_group_by_hashtag(cls, session):
        hashtags =  session.query(HoloMemberHashtag.hashtag).filter(HoloMemberHashtag.isUse == "Y").group_by(HoloMemberHashtag.hashtag).all()
        LOG.info("len list : {}".format(len(hashtags)))
        return list(map(lambda i: i[0].strip(), hashtags))

    @classmethod
    def get_group_by_hashtag_not_use(cls, session):
        hashtags =  session.query(HoloMemberHashtag.hashtag).filter(HoloMemberHashtag.isUse == "N").group_by(HoloMemberHashtag.hashtag).all()
        LOG.info("len list : {}".format(len(hashtags)))
        return list(map(lambda i: i[0].strip(), hashtags))




    FIELDS = {"hashtag": str, "datatype": str, "type": str , 'member_id' : str}

    FIELDS.update(Base.FIELDS)
