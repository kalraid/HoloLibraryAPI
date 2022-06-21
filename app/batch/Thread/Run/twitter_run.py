import json
from collections import Awaitable
from datetime import datetime
import traceback
import time

from pymysql import IntegrityError
from sqlalchemy.exc import PendingRollbackError

from app.config import BACK_SERVER_URL

import websockets, asyncio, threading
from twitter import TwitterError
from websockets.exceptions import ConnectionClosed

import log
from app.batch.Thread.Service.twitter_parser import tweet_parse
from app.const import CONST
from app.database import get_session, new_session
from app.model import HoloMemberTwitterInfo, HoloMemberTwitterHashtag

import twitter

twitter_api = twitter.Api(consumer_key=CONST.TWITTER_CONSUMER_KEY,
                          consumer_secret=CONST.TWITTER_CONSUMER_SECRET,
                          access_token_key=CONST.TWITTER_ACCESS_TOKEN,
                          access_token_secret=CONST.TWITTER_ACCESS_SECRET)

account = ["8803178971249188864", "1433414457179312128"]
sending_list = []
LOG = log.get_logger()


def twitter_run():
    ## Note(chp) twitter subthreading
    t = Worker("twitter_subthread")
    t.start()

    ## Note(chp) websocket async
    asyncio.run(init_websocket())


class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name  # thread 이름 지정

    def run(self):
        twitter_subthread()


def twitter_subthread():
    db_session = get_session()

    LOG.info("twitter_run start")

    # 홀로 멤버 트위터 id 리스트
    account = HoloMemberTwitterInfo().get_twitter_ids(db_session)

    # HoloMemberTwitterHashtag 중 isUse 가 N인 리스트
    ban_tags = HoloMemberTwitterHashtag().get_group_by_hashtag_not_use(db_session)

    # 스트림 호출
    stream = twitter_api.GetStreamFilter(follow=account, filter_level="low")
    twitter_api.GetUserStream()

    while True:
        try:
            for tweets in stream:
                if "user" in tweets and "id" in tweets["user"]:
                    twitter_id = str(tweets["user"]["id"])

                    # 멤버 계정이 적은 트윗인 경우만
                    if twitter_id in account:
                        # 받아온 트윗 내용을 DB 저장을 위한 HoloMemberTweet 객체로 전환
                        tweet_parse_result = tweet_parse(tweets, ban_tags)
                        # LOG.info("tweet_parse_result : {}".format(tweet_parse_result))

                        if tweet_parse_result:
                            db_session.add(tweet_parse_result)
                            db_session.commit()

                            # 받아온 트윗을 socket을 통해 서버로 전달할 데이터 객체
                            sending_data = {"tweet_id": tweet_parse_result.tweet_id,
                                            "member_id": tweet_parse_result.holo_member_twitter_info.member_id}
                            sending_list.append(sending_data)
                            LOG.info(" ----| sending_list data insert |----")

        except TwitterError as ex:  # Exceeded connection limit for user
            time.sleep(60 * 11)  # 11 minutes 대기 ( 트위터 api 중에 종료요청이 없기에 의도적 타임 슬립으로 트위터에서 종료되게 해야됨 )
            LOG.error(traceback.format_exc())
            LOG.error(str(stream))

            # 스트림 재시작
            stream = twitter_api.GetStreamFilter(follow=account, filter_level="low")
            twitter_api.GetUserStream()

            # 문제된 세션 종료 후 다시 받아오기
            # db_session = get_session()
            db_session = new_session(db_session)
        except IntegrityError or PendingRollbackError as ex:  # tweet_id 중복 나는 경우  스트림이 터진건 아니기에 유지
            LOG.error(traceback.format_exc())
            LOG.error(ex)

            # 문제된 세션 종료 후 다시 받아오기
            # db_session = get_session()
            db_session = new_session(db_session)

        except Exception as ex:
            LOG.error(traceback.format_exc())
            LOG.error(stream)


async def init_websocket():
    LOG.info("twitter_run init_websocket start ")
    while True:
        try:
            async with websockets.connect("ws://" + BACK_SERVER_URL + ":8000/v1/member/tweet/live",
                                          subprotocols=["live_tweet"],
                                          ping_interval=10, ping_timeout=60 * 60) as ws:
                LOG.info("twitter websocket standing ")
                while True:
                    try:
                        if len(sending_list) > 0:
                            i = sending_list.pop()
                            result = await ws.send(json.dumps(i))
                            LOG.info(f'websocket result : {result}')
                            message = await ws.recv()
                            LOG.info(f'websocket message : {message} ')
                    except Exception as ex:
                        LOG.error(traceback.format_exc())
                        LOG.error(ex)
        except ConnectionClosed:
            LOG.info("----| ConnectionClosed - reconnect |----")
            continue
