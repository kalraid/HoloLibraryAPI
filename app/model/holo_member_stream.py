# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, DATE
from sqlalchemy.orm import relationship

from app.model import Base


class HoloMemberStream(Base):
    __tablename__ = 'holo_member_stream'

    id = Column(Integer, primary_key=True)

    member_id = Column(Integer, ForeignKey('holo_member.index'))
    member = relationship("HoloMember", backref="holo_member_stream")

    # item.id.videoId
    video_id = Column(String(50), nullable=False)
    # item.id.videoId
    video_id = Column(String(50), nullable=False)

    start_date = Column(DATE, nullable=True)
    end_date = Column(DATE, nullable=True)
    #
    # pageInfo.totalResults
    # pageInfo.resultsPerPage
    # snippet.publishedAt
    # snippet.channelId
    # snippet.title
    #
    # snippet.thumbnails.dafault.url
    # snippet.channelTitle
    #
    # snippet.channelId
    # snippet.title
    # snippet.description
    # snippet.publishedAt
    # snippet.channelTitle
    # snippet.thumbnails.high.url
    # snippet.liveBroadcastContent

    def __repr__(self):
        return "<HoloMemberStream(id='%s', name='%s', member_name='%s', start_date='%s', end_date='%s')>" % (
            self.id,
            self.name,
            self.member_name,
            self.start_date,
            self.end_date,
        )

    @classmethod
    def get_id(cls):
        return HoloMemberStream.id

    @classmethod
    def get_name(cls):
        return HoloMemberStream.name


    FIELDS = {"id": str, "email": str, "name": str, "start_date": DATE,"end_date": DATE }

    FIELDS.update(Base.FIELDS)