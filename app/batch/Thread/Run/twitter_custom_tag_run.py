import asyncio

import websockets
from requests.exceptions import ChunkedEncodingError
from twitter import TwitterError
from websockets.exceptions import ConnectionClosed

import log

import traceback

from app.database import get_session
from app.model import HoloMemberTwitterHashtag, HoloTwitterDraw, HoloMemberHashtag, HoloTwitterDrawHashtag, \
    HoloTwitterCustomDraw, HoloTwitterCustomDrawHashtag
import threading

import time
import sched

twitter_consumer_key = "LyJRYgDOXyXgkEwVfCzZdvYZx"
twitter_consumer_secret = "GJqGw39xTKs63CQB84vvxuhAnLifVPIkeYHehNH7pypGwGqjoq"
# twitter_access_token = "AAAAAAAAAAAAAAAAAAAAAHsjTgEAAAAAWiB8zHi6GLqE1aF%2F4yNtd8kMqnQ%3DXBQE9cq3pSVn0PrT9ln4vmLyqsGNeuTAuril09anUvI1qifuUg"
twitter_access_token = "1433414457179312128-Rk4M7AhwcoOS5l4vGLHpGhZPU5RT6Y"
twitter_access_secret = "MOsBpp5QYq8lhwZXGdXsDNTrSftcAod7kAoPSRVC5f5hh"
import twitter

twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret,
                          access_token_key=twitter_access_token,
                          access_token_secret=twitter_access_secret)

import json

account = ["8803178971249188864", "1433414457179312128"]
output_file_name = "../../../../tests/stream_tag_result.txt"
db_session = get_session()
LOG = log.get_logger()

sending_list = []


def getHashTags():
    global stream
    tags = []
    try:
        hashTags = HoloMemberTwitterHashtag().get_group_by_hashtag_two_month(db_session)
        base_tags = HoloMemberHashtag().get_group_by_hashtag(db_session)
        for i in hashTags:
            if i not in base_tags:
                tags.append(i)
    except Exception:
        LOG.error(traceback.format_exc())
        LOG.error(stream)

    return tags


def twitter_custom_tag_run():
    LOG.info("twitter_custom_tag_run start")
    tags = getHashTags()

    if tags:
        ban_tags = HoloMemberTwitterHashtag().get_group_by_hashtag_not_use(db_session)

        LOG.info(" tags len : {} ".format(len(tags)))
        stream = twitter_api.GetStreamFilter(track=tags, filter_level="low")  # tags len max is 250
        twitter_api.GetUserStream()

        while True:
            try:
                for tweets in stream:
                    if "text" in tweets and tweets["text"] and tweets["text"][0:2] != "RT":  # post tweet only parsing
                        if "retweeted_status" not in tweets and "quoted_status" not in tweets:
                            entities = tweets["entities"]

                            if "extended_tweet" in tweets:
                                extend = tweets["extended_tweet"]
                                if "media" in extend:
                                    entities["media"] = extend["media"]
                                if "hashtags" in extend:
                                    entities["hashtags"] = extend["hashtags"]

                            hashtags = []
                            if entities is not None and "hashtags" in entities and entities["hashtags"]:
                                # holoMemberTweet.hashtags = list(set(map(lambda i: i["text"], entities["hashtags"])))
                                for i in entities["hashtags"]:
                                    holoTwitterDrawHashtag = HoloTwitterCustomDrawHashtag()
                                    holoTwitterDrawHashtag.hashtag = "#" + i["text"]
                                    holoTwitterDrawHashtag.datatype = "image"
                                    holoTwitterDrawHashtag.tagtype = "image"

                                    if i in ban_tags:
                                        holoTwitterDrawHashtag.isUse = "N"

                                    hashtags.append(holoTwitterDrawHashtag)

                            if "media" in entities and entities["media"]:
                                media = []
                                for i in entities["media"]:
                                    holo_twitter_draw = HoloTwitterCustomDraw()
                                    holo_twitter_draw.twitter_id = tweets["id"]
                                    holo_twitter_draw.url = i["media_url"]
                                    holo_twitter_draw.hashtag = hashtags

                                    holo_twitter_draw.twitter_user_nm = tweets['user']['screen_name']
                                    holo_twitter_draw.twitter_user_id = tweets['user']['id']
                                    media.append(holo_twitter_draw)

                                for i in media:
                                    db_session.add(i)
                                    for draw_tags in hashtags:
                                        draw_tags.holo_twitter_custom_draw = i
                                        db_session.add(draw_tags)
                                    # sending_data = {"custom_twitter_id": i.twitter_id,
                                    #                 "type": "test"}
                                    # sending_list.append(sending_data)
                                db_session.commit()

            except ChunkedEncodingError as ex:  # Connection broken -> restart
                LOG.error(traceback.format_exc())
                LOG.error(stream)
                tags = getHashTags()
                ban_tags = HoloMemberTwitterHashtag().get_group_by_hashtag_not_use(db_session)
                LOG.info(" tags len : {} ".format(len(tags)))
                stream = twitter_api.GetStreamFilter(track=tags, filter_level="low")  # tags len max is 250
                twitter_api.GetUserStream()
            except TwitterError as ex:  # Exceeded connection limit for user
                time.sleep(1 * 60 * 5)  # 5 minutes
                LOG.error(traceback.format_exc())
                LOG.error(stream)
                tags = getHashTags()
                ban_tags = HoloMemberTwitterHashtag().get_group_by_hashtag_not_use(db_session)
                LOG.info(" tags len : {} ".format(len(tags)))
                stream = twitter_api.GetStreamFilter(track=tags, filter_level="low")  # tags len max is 250
                twitter_api.GetUserStream()
    else:
        LOG.info("tags is empty")
