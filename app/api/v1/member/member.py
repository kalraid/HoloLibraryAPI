# -*- coding: utf-8 -*-

import json

from falcon.asgi import Request, WebSocket
from falcon.errors import WebSocketDisconnected

import log
from app.api.common import BaseResource
from app.model import UserStaticYoutube, HoloMemberCh, HoloMember, HoloMemberHashtag, HoloMemberTweet, \
    HoloMemberTwitterInfo, HoloMemberImage
from app.utils import alchemy

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
            member_dbs = session.query(HoloMember, HoloMemberImage.img_url) \
                .join(HoloMemberImage,HoloMemberImage.member_id == HoloMember.index). \
                filter(HoloMemberImage.img_type == 'small').filter(HoloMember.index == member_index).\
                filter(HoloMember.isUse == 'Y').first()
            filters['member_index'] = member_index

        elif 'member_id' in params and params['member_id']:
            member_id = params['member_id']
            member_dbs = session.query(HoloMember, HoloMemberImage.img_url). \
                join(HoloMemberImage, HoloMemberImage.member_id == HoloMember.index). \
                filter(HoloMemberImage.img_type == 'small').filter(HoloMember.index == member_id). \
                filter(HoloMember.isUse == 'Y').first()
            filters['member_index'] = member_id

        elif 'member_name_kor' in params and params['member_name_kor']:
            member_name_kor = params['member_name_kor']
            member_dbs = session.query(HoloMember, HoloMemberImage.img_url).join(HoloMemberImage,
                                                                                 HoloMemberImage.member_id == HoloMember.index).filter(
                HoloMemberImage.img_type == 'small').filter(HoloMember.member_name_kor == member_name_kor). \
                filter(HoloMember.isUse == 'Y').first()
            filters['member_name_kor'] = member_name_kor

        elif 'member_name_eng' in params and params['member_name_eng']:
            member_name_eng = params['member_name_eng']
            member_dbs = session.query(HoloMember, HoloMemberImage.img_url).join(HoloMemberImage,
                                                                                 HoloMemberImage.member_id == HoloMember.index).filter(
                HoloMemberImage.img_type == 'small').filter(HoloMember.member_name_eng == member_name_eng). \
                filter(HoloMember.isUse == 'Y').first()
            filters['member_name_eng'] = member_name_eng

        elif 'member_name' in params and params['member_name']:
            member_name = params['member_name']
            member_dbs = session.query(HoloMember, HoloMemberImage.img_url).join(HoloMemberImage,
                                                                                 HoloMemberImage.member_id == HoloMember.index). \
                filter(HoloMemberImage.img_type == 'small').filter(HoloMember.member_name_eng == member_name). \
                filter(HoloMember.isUse == 'Y').first()
            filters['member_name_eng'] = member_name
        else:
            member_dbs = session.query(HoloMember, HoloMemberImage.img_url). \
                join(HoloMemberImage, HoloMemberImage.member_id == HoloMember.index). \
                filter(HoloMember.isUse == 'Y').filter(HoloMemberImage.img_type == 'small').all()

        # data = alchemy.db_result_to_dict_list(member_dbs)
        list = []
        if type(list) == type(member_dbs) and len(member_dbs) > 1:
            for i in member_dbs:
                temp = i[0].to_dict()
                temp['img_url'] = i[1]

                list.append(temp)
        else:
            if member_dbs is not None and len(member_dbs) != 0:
                temp = member_dbs[0].to_dict()
                temp['img_url'] = member_dbs[1]

                list.append(temp)

        obj = {'len': len(list), 'filters': filters, 'member_list': list}
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


connection_clients = []


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
                .join(HoloMemberTwitterInfo,
                      HoloMemberTwitterInfo.twitter_id == HoloMemberTweet.holo_member_twitter_info_id) \
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
    Handle for endpoint: /v1/member/tweet/live
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params

        filters = {}
        if 'member_id' in params and params['member_id']:
            member_id = params['member_id']
            tweet_dbs = session.query(HoloMemberTweet, HoloMemberTwitterInfo.index) \
                .join(HoloMemberTwitterInfo) \
                .order_by(HoloMemberTweet.index.desc()).limit(1).all()

            filters['member_id'] = member_id
        elif 'type' in params and params['type'] == "only":
            tweet_dbs = session.query(HoloMemberTweet, HoloMemberTwitterInfo.index) \
                .join(HoloMemberTwitterInfo) \
                .order_by(HoloMemberTweet.index.desc()).limit(1).all()

            filters['type'] = params['type']
        else:
            tweet_dbs = session.query(HoloMemberTweet, HoloMemberTwitterInfo.index) \
                .join(HoloMemberTwitterInfo) \
                .order_by(HoloMemberTweet.index.desc()) \
                .group_by(HoloMemberTweet.holo_member_twitter_info_id).all()

        # list = alchemy.db_result_to_dict_list(tweet_dbs)
        list = []
        if type(list) == type(tweet_dbs) and len(tweet_dbs) > 1:
            for i in tweet_dbs:
                temp = i[0].to_dict()
                if temp['rt_tweet_id'] is not None:
                    temp['tweet_id'] = temp['rt_tweet_id']
                temp['member_id'] = i[1]

                list.append(temp)
        else:
            if tweet_dbs is not None and len(tweet_dbs) != 0:
                temp = tweet_dbs[0][0].to_dict()
                if 'rt_tweet_id' in temp and temp['rt_tweet_id'] is not None:
                    temp['tweet_id'] = temp['rt_tweet_id']

                temp['member_id'] = tweet_dbs[0][1]

                list.append(temp)

        obj = {'len': len(list), 'filters': filters, 'tweet_list': list}
        self.on_success(res, obj)

    async def on_websocket(self, req: Request, socket: WebSocket):
        global connection_clients
        LOG.info("----- /v1/member/tweet/live websocket init start ---------")
        LOG.info(req)

        # any headder is websocket close rule
        # some_header_value = req.get_header('Some-Header')
        #
        # if some_header_value:
        #
        #     await socket.close()
        #     return
        # Examine subprotocols advertised by the client. Here let's just
        #   assume we only support wamp, so if the client doesn't advertise
        #   it we reject the connection.
        if 'live_tweet' not in socket.subprotocols:
            # If close() is not called explicitly, the framework will
            #   take care of it automatically with the default code (1000).
            return

        # If, after examining the connection info, you would like to accept
        #   it, simply call accept() as follows:

        try:
            await socket.accept(subprotocol='live_tweet')
            connection_clients.append(socket)
            LOG.info(connection_clients)
        except WebSocketDisconnected:
            LOG.error("member websocket WebSocketDisconnected - not accepted")
            if socket in connection_clients:
                connection_clients.remove(socket)
                LOG.info(connection_clients)
            return
        # simple send
        while True:
            try:
                # LOG.info(f"---|  socket.ready :{socket.ready}  |--- ")
                # listen by batch

                # payload_str = await socket.receive_text()
                media_object = await socket.receive_media()
                # LOG.info(f'---| media_object : {media_object} |--- ')
                # send to web

                # await socket.send_text(event)  # TEXT
                for i in connection_clients:
                    sending = await i.send_media(media_object)
                # LOG.info(f'---|  sending : {media_object}  |--- ')

            except WebSocketDisconnected:
                LOG.error("member websocket WebSocketDisconnected")
                if socket in connection_clients:
                    connection_clients.remove(socket)
                    LOG.info(connection_clients)
                # Do any necessary cleanup, then bail out
                return
            except TypeError:
                LOG.error("member websocket TypeError")

                # The received message payload was not of the expected
                #   type (e.g., got BINARY when TEXT was expected).
                pass
            except json.JSONDecodeError:
                LOG.error("member websocket JSONDecodeError")

                # The default media deserializer uses the json standard
                #   library, so you might see this error raised as well.
                pass


class Customes(BaseResource):
    """
    Handle for endpoint: /v1/member/customes
    """

    async def on_get(self, req, res):
        session = req.context["session"]
        params = req.params

        filters = {}
        if 'member_id' in params and params['member_id']:
            member_id = params['member_id']
            customes = session.query(HoloMemberImage) \
                .filter(HoloMemberImage.img_type == 'large') \
                .filter(HoloMemberImage.member_id == member_id).all()

            filters['member_id'] = member_id
        else:
            customes = session.query(HoloMemberImage) \
                .filter(HoloMemberImage.img_type == 'large').all()
        data = alchemy.db_result_to_dict_list(customes)

        obj = {'len': len(data), 'filters': filters, 'customes_list': data}
        self.on_success(res, obj)
