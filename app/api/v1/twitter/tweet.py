# -*- coding: utf-8 -*-
from sqlalchemy import func, desc

import log
from app.api.common import BaseResource
from app.errors import NotSupportedError
from app.model import HoloTwitterDraw, HoloMemberTwitterInfo, \
    HoloMemberTweet, HoloMemberHashtag, HoloTwitterDrawHashtag, HoloTwitterCustomDraw, HoloTwitterCustomDrawHashtag, \
    HoloMemberTwitterHashtag, HoloTwitterDrawHist
from app.utils import alchemy

LOG = log.get_logger()


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
                    .join(HoloTwitterDrawHashtag, HoloTwitterDrawHashtag.holo_twitter_draw_id == HoloTwitterDraw.index) \
                    .join(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterDrawHashtag.hashtag) \
                    .where(HoloMemberHashtag.member_id == member_id) \
                    .order_by(HoloTwitterDraw.created.desc()).limit(100) \
                    .all()

            filters['member_id'] = member_id
        elif 'draw_index' in params and params['draw_index']:
            draw_index = params['draw_index']
            draw_dbs = session.query(HoloTwitterDraw, HoloTwitterDrawHashtag.tagtype, HoloTwitterDrawHashtag.datatype,
                                     HoloMemberHashtag.hashtag, HoloMemberHashtag.member_id, HoloMemberHashtag.tagtype,
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


class DrawsLive(BaseResource):
    """
    Handle for endpoint: /v1/tweet/draws/live
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params
        filters = {}
        if 'type' in params and params['type']:

            type = params['type']
            LOG.info(f'type : {type}')
            if type == 'random':
                draw_dbs = session.query(HoloTwitterDraw) \
                    .join(HoloTwitterDrawHashtag) \
                    .join(HoloMemberHashtag, HoloTwitterDrawHashtag.hashtag == HoloMemberHashtag.hashtag) \
                    .where(HoloMemberHashtag.tagtype == 'fanart').order_by(func.rand()).limit(60 * 60).all()
            elif type == 'recomanded':
                Ids = session.query(HoloTwitterDrawHist.holo_twitter_draw_id) \
                    .group_by(HoloTwitterDrawHist.holo_twitter_draw_id) \
                    .where(HoloTwitterDrawHist.holo_twitter_draw_id != None) \
                    .order_by(desc(func.count(HoloTwitterDrawHist.index))) \
                    .limit(60 * 60).all()
                draw_dbs = session.query(HoloTwitterDraw).where(HoloTwitterDraw.index.in_(Ids)).limit(60 * 60).all()
            else:
                draw_dbs = session.query(HoloTwitterDraw).order_by(func.rand()).limit(60 * 60).all()

            filters['type'] = type
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

        # data = alchemy.db_result_to_dict_list(draw_dbs)
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
                        .where(HoloTwitterCustomDrawHashtag.hashtag.in_(hashtag_list)) \
                        .group_by(HoloTwitterCustomDraw.twitter_id).limit(5).all()

                else:
                    dbs = session.query(HoloTwitterDraw) \
                        .join(HoloTwitterDrawHashtag) \
                        .where(HoloTwitterDrawHashtag.hashtag.in_(hashtag_list)) \
                        .group_by(HoloTwitterDraw.twitter_id).limit(5).all()

                filters['tagtype'] = tagtype
            else:
                dbs = session.query(HoloTwitterDraw) \
                    .join(HoloTwitterDrawHashtag) \
                    .where(HoloTwitterDrawHashtag.hashtag.in_(hashtag_list)) \
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

            # custom tags + memberTweet tags - baseTags
            draw_tags_dbs = session.query(HoloTwitterCustomDrawHashtag) \
                .outerjoin(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterCustomDrawHashtag.hashtag) \
                .outerjoin(HoloMemberTwitterHashtag,
                           HoloMemberTwitterHashtag.hashtag == HoloTwitterCustomDrawHashtag.hashtag) \
                .join(HoloMemberTweet) \
                .join(HoloMemberTwitterInfo) \
                .filter(HoloMemberHashtag.hashtag == None) \
                .filter(HoloMemberTwitterHashtag.hashtag != None) \
                .filter(HoloMemberTwitterInfo.member_id.in_(member_list)) \
                .group_by(HoloTwitterCustomDrawHashtag.hashtag) \
                .order_by(HoloTwitterCustomDrawHashtag.index.desc()).limit(10) \
                .all()

            filters['member_id'] = memberId
        else:

            # custom tags + memberTweet tags - baseTags
            draw_tags_dbs = session.query(HoloTwitterCustomDrawHashtag) \
                .outerjoin(HoloMemberHashtag, HoloMemberHashtag.hashtag == HoloTwitterCustomDrawHashtag.hashtag) \
                .outerjoin(HoloMemberTwitterHashtag,
                           HoloMemberTwitterHashtag.hashtag == HoloTwitterCustomDrawHashtag.hashtag) \
                .filter(HoloMemberHashtag.hashtag == None) \
                .filter(HoloMemberTwitterHashtag.hashtag != None) \
                .group_by(HoloTwitterCustomDrawHashtag.hashtag) \
                .order_by(HoloTwitterCustomDrawHashtag.index.desc()).limit(10) \
                .all()

        list = alchemy.db_result_to_dict_list(draw_tags_dbs)

        obj = {'len': len(list), 'filters': filters, 'custom_tags': list}
        self.on_success(res, obj)
