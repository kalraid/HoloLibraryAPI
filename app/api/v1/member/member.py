# -*- coding: utf-8 -*-

import re

import falcon
import requests
from sqlalchemy.orm.exc import NoResultFound
from collections import defaultdict

import log, json
from app.api.common import BaseResource
from app.errors import (
    AppError,
    UserNotExistsError,
    PasswordNotMatch,
)
from app.utils import alchemy
from app.model import User, UserStaticYoutube, HoloMemberCh, HoloMember, HoloMemberHashtag, HoloMemberTweet, \
    HoloMemberTwitterInfo
from app.utils.auth import verify_password
from app.utils.hooks import auth_required

LOG = log.get_logger()

FIELDS = {
    "username": {"type": "string", "required": True, "minlength": 4, "maxlength": 20},
    "email": {
        "type": "string",
        "regex": "[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}",
        "required": True,
        "maxlength": 320,
    },
    "password": {
        "type": "string",
        "regex": "[0-9a-zA-Z]\w{3,14}",
        "required": True,
        "minlength": 8,
        "maxlength": 64,
    },
    "info": {"type": "dict", "required": False},
}


class Collection(BaseResource):
    """
    Handle for endpoint: /v1/member/youtube/channel/list
    """

    async def on_get(self, req, res):
        session = req.context["session"]

        queryString = dict()
        for key, value in req.params.items():
            queryString[key] = value;
            # LOG.info(f'key  : {key} , value : {value}, req.params : {req.params}, queryString : {queryString}')

        if queryString.get('user_id'):
            member_ch_dbs = session.query(HoloMemberCh, UserStaticYoutube.sub_date, HoloMember.member_classification,
                                          HoloMember.member_generation) \
                .join(UserStaticYoutube, UserStaticYoutube.channel_id == HoloMemberCh.channel_id) \
                .join(HoloMember, HoloMember.member_name_kor == HoloMemberCh.member_name).all()

            member_ch_list = []
            for i in member_ch_dbs:
                # LOG.info(f" type(i) : {type(i)}, i : {i[0]} , i[1] : {i[1]}")
                temp = i[0].to_dict()
                temp['sub_date'] = i[1].strftime('%Y-%m-%d')
                temp['class'] = i[2]
                temp['genera'] = i[3]
                member_ch_list.append(temp)


        else:
            member_ch_dbs = session.query(HoloMemberCh, HoloMember.member_classification, HoloMember.member_generation) \
                .join(HoloMember, HoloMember.member_name_kor == HoloMemberCh.member_name).all()
            member_ch_list = []
            for i in member_ch_dbs:
                temp = i[0].to_dict()
                temp['class'] = i[1]
                temp['genera'] = i[2]
                member_ch_list.append(temp)

        data = member_ch_list
        obj = {'data': data}
        self.on_success(res, obj)


class List(BaseResource):
    """
    Handle for endpoint: /v1/member/list
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params

        filters = {}
        if 'index' in params and params['index']:
            member_index = params['index']
            member_dbs = session.query(HoloMember).filter(HoloMember.index == member_index).first()
            filters['member_index'] = member_index

        elif 'member_id' in params and params['member_id']:
            member_id = params['member_id']
            member_dbs = session.query(HoloMember).filter(HoloMember.index == member_id).first()
            filters['member_index'] = member_id

        elif 'member_name_kor' in params and params['member_name_kor']:
            member_name_kor = params['member_name_kor']
            member_dbs = session.query(HoloMember).filter(HoloMember.member_name_kor == member_name_kor).first()
            filters['member_name_kor'] = member_name_kor

        elif 'member_name_eng' in params and params['member_name_eng']:
            member_name_eng = params['member_name_eng']
            member_dbs = session.query(HoloMember).filter(HoloMember.member_name_eng == member_name_eng).first()
            filters['member_name_eng'] = member_name_eng

        elif 'member_name' in params and params['member_name']:
            member_name = params['member_name']
            member_dbs = session.query(HoloMember).filter(HoloMember.member_name_eng == member_name).first()
            filters['member_name_eng'] = member_name
        else:
            member_dbs = session.query(HoloMember).all()

        data = alchemy.db_result_to_dict_list(member_dbs)

        obj = {'len': len(data), 'filters': filters, 'member_list': data}
        self.on_success(res, obj)


class Tags(BaseResource):
    """
    Handle for endpoint: /v1/member/tags
    """

    # params = queryString , pathParm = req.path

    async def on_get(self, req, res):
        session = req.context["session"]
        # member_id = req.path
        # LOG.info(f'req.path : {req.path}, member_id : {member_id}')
        params = req.params
        filters = {}
        if 'member_id' in params and params['member_id']:
            member_id = params['member_id']
            LOG.info(f'-------------------  member_id : {member_id}')
            tag_dbs = session.query(HoloMemberHashtag).filter(HoloMemberHashtag.member_id == member_id).all()
            filters['member_id'] = member_id
        elif 'index' in params and params['index']:
            index = params['index']
            tag_dbs = session.query(HoloMemberHashtag).filter(HoloMemberHashtag.member_id == index).all()
            filters['member_id'] = index
        else:
            tag_dbs = session.query(HoloMemberHashtag).all()

        data = alchemy.db_result_to_dict_list(tag_dbs)

        obj = {'len': len(data), 'filters': filters, 'tag_list': data}
        self.on_success(res, obj)



class Tweets(BaseResource):
    """
    Handle for endpoint: /v1/member/tweets
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params

        filters = {}
        if 'member_id' in params and params['member_id']:
            member_id = params['member_id']
            tweet_dbs = session.query(HoloMemberTweet) \
                .join(HoloMemberTwitterInfo, HoloMemberTwitterInfo.twitter_id == HoloMemberTweet.holo_member_twitter_info_id) \
                .filter(HoloMemberTwitterInfo.member_id == member_id) \
                .order_by(HoloMemberTweet.created.desc()).limit(100).all()

            filters['member_id'] = member_id
        else:
            tweet_dbs = session.query(HoloMemberTweet).order_by(HoloMemberTweet.created.desc()).limit(100).all()

        data = alchemy.db_result_to_dict_list(tweet_dbs)

        obj = {'len': len(data), 'filters': filters, 'tweet_list': data}
        self.on_success(res, obj)


class TweetLive(BaseResource):
    """
    Handle for endpoint: /v1/member/tweet/live/{member_id}
    """

    async def on_get(self, req, res):
        session = req.context["session"]

        # TODO get web socket for real time tweet

        obj = {'data': None}
        self.on_success(res, obj)
