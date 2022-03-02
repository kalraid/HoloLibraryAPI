# -*- coding: utf-8 -*-
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased

import log
from app.api.common import BaseResource
from app.errors import NotSupportedError
from app.model import HoloTwitterDraw, HoloMemberTwitterInfo, \
    HoloMemberTweet, HoloMemberHashtag, HoloTwitterDrawHashtag, HoloTwitterCustomDraw, HoloTwitterCustomDrawHashtag, \
    HoloMemberTwitterHashtag, DrawStatistics, HoloMemberTwitterMedia
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

                draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.tagtype,
                                         HoloTwitterDrawHashtag.datatype,
                                         HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id,
                                         HoloMemberHashtag.tagtype,
                                         HoloMemberHashtag.datatype) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .filter(HoloMemberHashtag.member_id == member_id) \
                    .filter(HoloMemberHashtag.tagtype.in_(type_list)) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(12 * 50) \
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
                    .filter(HoloMemberHashtag.member_id == member_id) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(100) \
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
                .order_by(HoloTwitterDraw.created.desc()).limit(100) \
                .all()

            filters['draw_index'] = draw_index
        else:
            draw_dbs = session.query(HoloTwitterDraw).filter(HoloTwitterDraw.isUse == 'Y'). \
                order_by(HoloTwitterDraw.created.desc()).limit(100).all()

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
                draw_dbs = session.query(HoloTwitterDraw) \
                    .join(HoloTwitterDrawHashtag) \
                    .join(HoloMemberHashtag, HoloTwitterDrawHashtag.hashtag == HoloMemberHashtag.hashtag) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .filter(HoloMemberHashtag.tagtype.in_(tagTypes)).order_by(func.rand()).limit(60 * 60).all()
            elif type == 'recommend':
                LOG.info(f'recommend type : {type}, tagType : {tagTypes}')
                Ids = session.query(DrawStatistics.holo_twitter_draw_id) \
                    .group_by(DrawStatistics.holo_twitter_draw_id) \
                    .filter(DrawStatistics.holo_twitter_draw_id is not None) \
                    .filter(HoloMemberHashtag.tagtype.in_(tagTypes)) \
                    .order_by(desc(func.count(DrawStatistics.index))) \
                    .limit(60 * 60)

                draw_dbs = session.query(HoloTwitterDraw) \
                    .filter(HoloTwitterDraw.isUse == 'Y') \
                    .join(Ids) \
                    .limit(60 * 60).all()
            else:
                draw_dbs = session.query(HoloTwitterDraw).order_by(func.rand()).limit(60 * 60).all()

            filters['type'] = type
            filters['tagType'] = type_param
        else:
            raise NotSupportedError("GET", "/v1/tweet/draws/live")

        list = alchemy.db_result_to_dict_list(draw_dbs)

        obj = {'len': len(list), 'filters': filters, 'tweet_list': list}
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
                .limit(600).all()

            third_draws = session.query(HoloTwitterCustomDraw) \
                .join(HoloTwitterCustomDrawHashtag) \
                .filter(HoloTwitterCustomDrawHashtag.hashtag.in_(tag_list)) \
                .filter(HoloTwitterCustomDraw.isUse == 'Y') \
                .limit(600).all()

            filters['hashtags'] = hashtags


        else:
            second_draws = session.query(HoloMemberTwitterMedia) \
                .join(HoloMemberTweet) \
                .join(HoloMemberTwitterHashtag) \
                .filter(HoloMemberTwitterMedia.media_type == 'img') \
                .filter(HoloMemberTwitterMedia.isUse == 'Y') \
                .limit(600).all()

            third_draws = session.query(HoloTwitterCustomDraw) \
                .join(HoloTwitterCustomDrawHashtag) \
                .filter(HoloTwitterCustomDraw.isUse == 'Y') \
                .limit(600).all()

        list = alchemy.db_result_to_dict_list(second_draws)
        data = alchemy.db_result_to_dict_list(third_draws)

        obj = {'len': len(list) + len(data), 'filters': filters, 'second_draws': list, 'third_draws': data}
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
