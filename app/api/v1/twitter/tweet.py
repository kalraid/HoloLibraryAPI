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
from app.model import User, UserStaticYoutube, HoloMemberCh, HoloMember, HoloTwitterDraw, HoloMemberTwitterInfo, \
    HoloMemberTweet, HoloMemberHashtag, HoloTwitterDrawHashtag, HoloTwitterCustomDraw, HoloTwitterCustomDrawHashtag, \
    HoloMemberTwitterHashtag
from app.utils import alchemy
from app.utils.auth import verify_password
from app.utils.hooks import auth_required

LOG = log.get_logger()


class Draws(BaseResource):
    """
    Handle for endpoint: /v1/tweet/draws
    """

    def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}
        if 'member_id' in params and params['member_id']:

            member_id = params['member_id']

            if 'hashtags' in params and params['hashtags']:
                hashtags = params['hashtags']

                draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.type, HoloTwitterDrawHashtag.datatype,
                                         HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id, HoloMemberHashtag.type,
                                         HoloMemberHashtag.datatype) \
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .filter(HoloMemberHashtag.member_id == member_id) \
                    .filter(HoloMemberHashtag.hashtag.in_(hashtags)) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(100) \
                    .all()
                filters['hashtags'] = hashtags

            elif 'type' in params and params['type']:
                type_param = params['type']
                type_list = []
                for type_str in type_param.split(','):
                    type_list.append(type_str.strip())

                draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.type, HoloTwitterDrawHashtag.datatype,
                                         HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id, HoloMemberHashtag.type,
                                         HoloMemberHashtag.datatype) \
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .filter(HoloMemberHashtag.member_id == member_id) \
                    .filter(HoloMemberHashtag.type.in_(type_list)) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(100) \
                    .all()
                filters['type'] = type_param

            else:
                draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.type, HoloTwitterDrawHashtag.datatype,
                                         HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id, HoloMemberHashtag.type,
                                         HoloMemberHashtag.datatype) \
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .where(HoloMemberHashtag.member_id == member_id) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(100) \
                    .all()

            filters['member_id'] = member_id
        elif 'draw_index' in params and params['draw_index']:
            draw_index = params['draw_index']
            draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.type, HoloTwitterDrawHashtag.datatype,
                                     HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id, HoloMemberHashtag.type,
                                     HoloMemberHashtag.datatype) \
                .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                .where(HoloTwitterDraw.index == draw_index) \
                .order_by(HoloTwitterDraw.created.desc()).limit(100) \
                .all()

            filters['draw_index'] = draw_index
        else:
            draw_dbs = session.query(HoloTwitterDraw).order_by(HoloTwitterDraw.created.desc()).limit(100).all()

        # data = alchemy.db_result_to_dict_list(draw_dbs)
        list = []
        if type(list) == type(draw_dbs):
            for i in draw_dbs:
                temp = i[0].to_dict()
                temp['tag_type'] = i[1]
                temp['tag_datatype'] = i[2]
                temp['hashtag'] = i[3]
                temp['member_id'] = i[4]
                temp['memtag_type'] = i[5]
                temp['memtag_datatype'] = i[6]

                list.append(temp)
        else:
            if draw_dbs is not None and len(draw_dbs) != 0:
                temp = draw_dbs[0].to_dict()
                temp['tag_type'] = draw_dbs[1]
                temp['tag_datatype'] = draw_dbs[2]
                temp['hashtag'] = draw_dbs[3]
                temp['member_id'] = draw_dbs[4]
                temp['memtag_type'] = draw_dbs[5]
                temp['memtag_datatype'] = draw_dbs[6]

                list.append(temp)

        obj = {'len': len(list), 'filters': filters, 'draw_list': list}
        self.on_success(res, obj)


class DrawsLive:
    """
    Handle for endpoint: /v1/tweet/draws/live
    """

    def on_get(self, req, res):
        session = req.context["session"]

        # TODO get web socket for real time tweet draws

        obj = {'data': None}
        self.on_success(res, obj)


class CustomDraws(BaseResource):
    """
    Handle for endpoint: /v1/tweet/custom/draws
    """

    def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        if 'hashtags' in params and params['hashtags']:
            hashtags = params['hashtags']

            tag_list = []
            for tag_str in hashtags.split(','):
                tag_list.append(tag_str.strip())

            draw_dbs = session.query(HoloTwitterCustomDraw, HoloTwitterCustomDrawHashtag.hashtag) \
                .join(HoloTwitterCustomDrawHashtag,
                      HoloTwitterCustomDrawHashtag.holo_twitter_custom_draw_id == HoloTwitterCustomDraw.index) \
                .filter(HoloTwitterCustomDrawHashtag.hashtag.in_(tag_list)) \
                .order_by(HoloTwitterCustomDraw.created.desc()).limit(100) \
                .all()

            filters['hashtags'] = hashtags


        else:
            draw_dbs = session.query(HoloTwitterCustomDraw, HoloTwitterCustomDrawHashtag.hashtag) \
                .join(HoloTwitterCustomDrawHashtag,
                      HoloTwitterCustomDrawHashtag.holo_twitter_custom_draw_id == HoloTwitterCustomDraw.index) \
                .order_by(HoloTwitterCustomDraw.created.desc()).limit(500) \
                .all()

        #data = alchemy.db_result_to_dict_list(draw_dbs)
        list = []
        if type(list) == type(draw_dbs):
            for i in draw_dbs:
                temp = i[0].to_dict()
                temp['hashtag'] = i[1]
                list.append(temp)
        else:
            if draw_dbs is not None and len(draw_dbs) != 0:
                temp = draw_dbs[0].to_dict()
                temp['hashtag'] = draw_dbs[1]

                list.append(temp)

        obj = {'len': len(list), 'filters': filters, 'draw_list': list}
        self.on_success(res, obj)


class CustomTags(BaseResource):
    """
    Handle for endpoint: /v1/tweet/custom/tags
    """

    def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        # HoloTwitterCustomDrawHashtag의 태그 중 holo_member_twitter_hashtag 에 존재하면서, holo_member_hashtag 에는 존재하지 않고
        # 2달 이내에 올라온 리스트를 카운트 순으로 order by 해서 50개를 해시태그만
        draw_tags_dbs = session.query(HoloTwitterCustomDrawHashtag) \
            .outerjoin(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterCustomDrawHashtag.hashtag) \
            .outerjoin(HoloMemberTwitterHashtag,
                       HoloMemberTwitterHashtag.hashtag == HoloTwitterCustomDrawHashtag.hashtag) \
            .filter(HoloMemberHashtag.hashtag == None) \
            .filter(HoloMemberTwitterHashtag.hashtag != None) \
            .group_by(HoloTwitterCustomDrawHashtag.hashtag) \
            .limit(50) \
            .all()

        list = alchemy.db_result_to_dict_list(draw_tags_dbs)

        obj = {'len': len(list), 'filters': filters, 'custom_tags': list}
        self.on_success(res, obj)
