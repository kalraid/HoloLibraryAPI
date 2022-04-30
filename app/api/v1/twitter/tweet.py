# -*- coding: utf-8 -*-
import random
import datetime

from sqlalchemy import func, desc, text
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

import log
from app.api.common import BaseResource
from app.api.common.base import SessionCommonAlias
from app.errors import NotSupportedError
from app.model import HoloTwitterDraw, HoloMemberTwitterInfo, \
    HoloMemberTweet, HoloMemberHashtag, HoloTwitterDrawHashtag, HoloTwitterCustomDraw, HoloTwitterCustomDrawHashtag, \
    HoloMemberTwitterHashtag, DrawStatistics, HoloMemberTwitterMedia, DrawStatisticsMenual
from app.utils import alchemy

LOG = log.get_logger()


class TwitterList(BaseResource):
    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        twitterInfos = session.query(HoloMemberTwitterInfo).all()

        data = alchemy.db_result_to_dict_list(twitterInfos)

        obj = {'len': len(data), 'filters': filters, 'twitter_list': data}
        self.on_success(res, obj)


class Draws(BaseResource):
    """
    Handle for endpoint: /v1/tweet/draws
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}
        if 'member_id' in params and params['member_id']:

            member_id = params['member_id']

            alias = SessionCommonAlias.ban_images(self, session)
            LOG.info(alias)

            if 'hashtags' in params and params['hashtags']:
                hashtags = params['hashtags']

                draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.tagtype,
                                         HoloTwitterDrawHashtag.datatype,
                                         HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id,
                                         HoloMemberHashtag.tagtype,
                                         HoloMemberHashtag.datatype) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .outerjoin(alias, alias.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .filter(alias.holo_twitter_draw_id == None) \
                    .filter(HoloMemberHashtag.hashtag.in_(hashtags)) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(60000) \
                    .all()
                filters['hashtags'] = hashtags

            elif 'type' in params and params['type']:
                type_param = params['type']
                type_list = []
                for type_str in type_param.split(','):
                    type_list.append(type_str.strip())

                draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.tagtype,
                                         HoloTwitterDrawHashtag.datatype,
                                         HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id,
                                         HoloMemberHashtag.tagtype,
                                         HoloMemberHashtag.datatype) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .outerjoin(alias, alias.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .filter(alias.holo_twitter_draw_id == None) \
                    .filter(HoloMemberHashtag.member_id == member_id) \
                    .filter(HoloMemberHashtag.tagtype.in_(type_list)) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(60000) \
                    .all()
                filters['type'] = type_param

            else:
                draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.tagtype,
                                         HoloTwitterDrawHashtag.datatype,
                                         HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id,
                                         HoloMemberHashtag.tagtype,
                                         HoloMemberHashtag.datatype) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .outerjoin(alias, alias.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .filter(alias.holo_twitter_draw_id == None) \
                    .filter(HoloMemberHashtag.member_id == member_id) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(60000) \
                    .all()

            filters['member_id'] = member_id
        elif 'draw_index' in params and params['draw_index']:
            draw_index = params['draw_index']
            draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.tagtype, HoloTwitterDrawHashtag.datatype,
                                     HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id, HoloMemberHashtag.tagtype,
                                     HoloMemberHashtag.datatype) \
                .filter(HoloTwitterDraw.isUse == 'Y') \
                .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                .filter(HoloTwitterDraw.index == draw_index) \
                .order_by(HoloTwitterDraw.created.desc()).limit(60000) \
                .all()

            filters['draw_index'] = draw_index
        else:
            draw_dbs = session.query(HoloTwitterDraw).filter(HoloTwitterDraw.isUse == 'Y'). \
                order_by(HoloTwitterDraw.created.desc()).limit(60000).all()

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

        obj = {'len': len(list), 'filters': filters, 'draw_list': list, 'draw_type': 'first'}
        self.on_success(res, obj)


class DrawsLive(BaseResource):
    """
    Handle for endpoint: /v1/tweet/draws/live
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}
        LOG.info(params)
        if 'type' in params and params['type'] and 'tagType' in params and params['tagType']:

            type_param = params['tagType']
            tagTypes = []
            for type_str in type_param.split(','):
                tagTypes.append(type_str.strip())

            type = params['type']
            if type == 'random':
                LOG.info(f'random type : {type}, tagType : {tagTypes}')
                number = str(round(datetime.datetime.now().timestamp()))[-2:]
                subquery = session.query(HoloTwitterDraw) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .filter(HoloTwitterDraw.index.like('%' + number[0])) \
                    .filter(HoloTwitterDraw.twitter_id.like('%' + number[1])) \
                    .subquery()
                alias = aliased(HoloTwitterDraw, subquery)

                subquery2 = session.query(HoloTwitterDrawHashtag) \
                    .join(HoloMemberHashtag, HoloTwitterDrawHashtag.hashtag == HoloMemberHashtag.hashtag) \
                    .filter(HoloMemberHashtag.tagtype.in_(tagTypes)) \
                    .subquery()
                alias2 = aliased(HoloTwitterDrawHashtag, subquery2)

                draw_dbs = session.query(alias) \
                    .join(alias2, alias.index == alias2.holo_twitter_draw_id) \
                    .limit(60 * 60) \
                    .all()

                random.shuffle(draw_dbs)

            elif type == 'recommend':
                LOG.info(f'recommend type : {type}, tagType : {tagTypes}')
                Ids = session.query(DrawStatistics.holo_twitter_draw_id) \
                    .group_by(DrawStatistics.holo_twitter_draw_id) \
                    .filter(DrawStatistics.holo_twitter_draw_id is not None) \
                    .filter(HoloMemberHashtag.tagtype.in_(tagTypes)) \
                    .order_by(desc(func.count(DrawStatistics.index))) \
                    .limit(60 * 60) \
                    .subquery()
                alias = aliased(DrawStatistics, Ids)

                draw_dbs = session.query(HoloTwitterDraw) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .join(alias) \
                    .filter(alias.index is not None) \
                    .all()
            else:
                draw_dbs = session.query(HoloTwitterDraw).filter(HoloTwitterDraw.isUse == 'Y').limit(60 * 60).all()
                random.shuffle(draw_dbs)

            filters['type'] = type
            filters['tagType'] = type_param
        else:
            raise NotSupportedError("GET", "/v1/tweet/draws/live")

        list = alchemy.db_result_to_dict_list(draw_dbs)

        obj = {'len': len(list), 'filters': filters, 'tweet_list': list, 'draw_type': 'first'}
        self.on_success(res, obj)


class CustomDraws(BaseResource):
    """
    Handle for endpoint: /v1/tweet/custom/draws
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        if 'hashtags' in params and params['hashtags']:
            hashtags = params['hashtags']

            tag_list = []
            for tag_str in hashtags.split(','):
                tag_list.append(tag_str.strip())

            # hashtag -> tweet id -> media + hashtag -> custom draw
            second_draws = session.query(HoloMemberTwitterMedia) \
                .join(HoloMemberTweet) \
                .join(HoloMemberTwitterHashtag) \
                .filter(HoloMemberTwitterHashtag.hashtag.in_(tag_list)) \
                .filter(HoloMemberTwitterMedia.media_type == 'img') \
                .filter(HoloMemberTwitterMedia.isUse == 'Y') \
                .order_by(HoloMemberTwitterMedia.created.desc()) \
                .limit(60000).all()

            third_draws = session.query(HoloTwitterCustomDraw) \
                .join(HoloTwitterCustomDrawHashtag) \
                .filter(HoloTwitterCustomDrawHashtag.hashtag.in_(tag_list)) \
                .filter(HoloTwitterCustomDraw.isUse == 'Y') \
                .order_by(HoloTwitterCustomDraw.created.desc()) \
                .limit(60000).all()

            filters['hashtags'] = hashtags


        else:
            second_draws = session.query(HoloMemberTwitterMedia) \
                .join(HoloMemberTweet) \
                .join(HoloMemberTwitterHashtag) \
                .filter(HoloMemberTwitterMedia.media_type == 'img') \
                .filter(HoloMemberTwitterMedia.isUse == 'Y') \
                .order_by(HoloMemberTwitterMedia.created.desc()) \
                .limit(60000).all()

            third_draws = session.query(HoloTwitterCustomDraw) \
                .join(HoloTwitterCustomDrawHashtag) \
                .filter(HoloTwitterCustomDraw.isUse == 'Y') \
                .order_by(HoloTwitterCustomDraw.created.desc()) \
                .limit(60000).all()

        list = alchemy.db_result_to_dict_list(second_draws)
        data = alchemy.db_result_to_dict_list(third_draws)

        obj = {'len': len(list) + len(data), 'filters': filters, 'second_draws': list, 'third_draws': data,
               'draw_type': 'second, third'}
        self.on_success(res, obj)


class TweetInfo(BaseResource):
    """
    Handle for endpoint: /v1/tweet/detail
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        if 'member_id' in params and params['member_id']:
            member_id = params['member_id']

            member_list = []
            for member_str in member_id.split(','):
                member_list.append(member_str.strip())

            draw_dbs = session.query(HoloMemberTwitterInfo) \
                .filter(HoloMemberTwitterInfo.member_id.in_(member_list)) \
                .all()

            filters['member_id'] = member_id

        else:
            draw_dbs = session.query(HoloMemberTwitterInfo) \
                .all()

        list = alchemy.db_result_to_dict_list(draw_dbs)

        obj = {'len': len(list), 'filters': filters, 'twitter_list': list}
        self.on_success(res, obj)


class TweetIds(BaseResource):
    """
    Handle for endpoint: /v1/tweet/ids
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        if 'hashtag' in params and params['hashtag']:
            hashtag = params['hashtag']
            hashtag_list = []
            filters['hashtag'] = hashtag

            for hashtag_str in hashtag.split(','):
                hashtag = hashtag_str.strip()
                if hashtag[0] != '#':
                    hashtag = '#' + hashtag
                hashtag_list.append(hashtag)

            if 'tagtype' in params and params['tagtype']:
                tagtype = params['tagtype']

                if 'custom' == tagtype:
                    dbs = session.query(HoloTwitterCustomDraw) \
                        .join(HoloTwitterCustomDrawHashtag) \
                        .filter(HoloTwitterCustomDrawHashtag.hashtag.in_(hashtag_list)) \
                        .group_by(HoloTwitterCustomDraw.twitter_id).limit(5).all()

                else:
                    dbs = session.query(HoloTwitterDraw) \
                        .join(HoloTwitterDrawHashtag) \
                        .filter(HoloTwitterDrawHashtag.hashtag.in_(hashtag_list)) \
                        .group_by(HoloTwitterDraw.twitter_id).limit(5).all()

                filters['tagtype'] = tagtype
            else:
                dbs = session.query(HoloTwitterDraw) \
                    .join(HoloTwitterDrawHashtag) \
                    .filter(HoloTwitterDrawHashtag.hashtag.in_(hashtag_list)) \
                    .group_by(HoloTwitterDraw.twitter_id).limit(5).all()

        list = alchemy.db_result_to_dict_list(dbs)

        obj = {'len': len(list), 'filters': filters, 'tweet_list': list}
        self.on_success(res, obj)


class CustomTags(BaseResource):
    """
    Handle for endpoint: /v1/tweet/custom/tags
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        if 'member_id' in params and params['member_id']:
            memberId = params['member_id']

            member_list = []
            for member_str in memberId.split(','):
                member_list.append(member_str.strip())

            subquery = session.query(HoloMemberTwitterHashtag) \
                .join(HoloMemberHashtag, HoloMemberTwitterHashtag.hashtag == HoloMemberHashtag.hashtag) \
                .filter(HoloMemberHashtag.member_id.in_(member_list)) \
                .filter(HoloMemberHashtag.hashtag != None).subquery()
            alias = aliased(HoloMemberTwitterHashtag, subquery)
            # second tag - first tag
            second_tags = session.query(alias) \
                .join(HoloMemberTweet) \
                .join(HoloMemberTwitterInfo) \
                .filter(HoloMemberTwitterInfo.member_id.in_(member_list)) \
                .order_by(alias.index.desc()).limit(10) \
                .all()

            filters['member_id'] = memberId

        else:

            subquery = session.query(HoloMemberTwitterHashtag) \
                .join(HoloMemberHashtag, HoloMemberTwitterHashtag.hashtag == HoloMemberHashtag.hashtag) \
                .filter(HoloMemberHashtag.hashtag != None).subquery()
            alias = aliased(HoloMemberTwitterHashtag, subquery)
            # second tag - first tag
            second_tags = session.query(alias) \
                .join(HoloMemberTweet) \
                .join(HoloMemberTwitterInfo) \
                .order_by(alias.index.desc()).limit(10) \
                .all()

        list = alchemy.db_result_to_dict_list(second_tags)

        obj = {'len': len(list), 'filters': filters, 'custom_tags': list}
        self.on_success(res, obj)


class RenewerDraws(BaseResource):
    """
    Handle for endpoint: /v1/tweet/renewer/draws
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}

        alias = SessionCommonAlias.ban_images(self, session)

        if 'tagType' in params and params['tagType']:
            tagType = params['tagType']
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

            draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.tagtype,
                                     HoloTwitterDrawHashtag.datatype,
                                     HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id,
                                     HoloMemberHashtag.tagtype,
                                     HoloMemberHashtag.datatype) \
                .filter(HoloTwitterDraw.isUse == 'Y') \
                .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                .outerjoin(alias, alias.holo_twitter_draw_id == HoloTwitterDraw.index) \
                .filter(alias.holo_twitter_draw_id == None) \
                .filter(HoloMemberHashtag.tagtype == tagType) \
                .filter(HoloTwitterDraw.created > yesterday) \
                .order_by(HoloTwitterDraw.created.desc()).limit(60000) \
                .all()
            filters['tagType'] = tagType

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

        obj = {'len': len(list), 'filters': filters, 'draw_list': list, 'draw_type': 'first'}
        self.on_success(res, obj)
