from datetime import datetime

import dateutil

import log
from app.database import get_session
from app.model import HoloMemberTweet, HoloMemberTwitterInfo

twitter_consumer_key = "LyJRYgDOXyXgkEwVfCzZdvYZx"
twitter_consumer_secret = "GJqGw39xTKs63CQB84vvxuhAnLifVPIkeYHehNH7pypGwGqjoq"
twitter_access_token = "1433414457179312128-Rk4M7AhwcoOS5l4vGLHpGhZPU5RT6Y"
twitter_access_secret = "MOsBpp5QYq8lhwZXGdXsDNTrSftcAod7kAoPSRVC5f5hh"

import twitter
import json

db_session = get_session()
test_list = list

LOG = log.get_logger()


def __init__():
    LOG.info("run start")
    twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                              consumer_secret=twitter_consumer_secret,
                              access_token_key=twitter_access_token,
                              access_token_secret=twitter_access_secret)

    account = ["880317891249188864", "1433414457179312128"]
    output_file_name = "stream_result.txt"
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        stream = twitter_api.GetStreamFilter(follow=account,
                                             filter_level='medium')  # GetStreamSample #GetUserStream
        while True:
            for tweets in stream:
                tweet_parse_result = tweet_parse(tweets)
                if tweet_parse_result:
                    db_session.add(tweet_parse_result)
                    test_list.add(tweet_parse_result)
                    db_session.commit()
                tweet = json.dumps(tweets, ensure_ascii=False)
                print(tweet, file=output_file, flush=True)


def tweet_parse(self, tweet):
    type = "BASE"
    holoMemberTweet = HoloMemberTweet()

    user = tweet["user"]
    if user["id"]:
        holoMemberTwitterInfo = HoloMemberTwitterInfo().find_by_twitter_info_id(db_session, user["id"])
        if holoMemberTwitterInfo is None:  # first tweet, but user id isn't member's id
            return None

        if holoMemberTwitterInfo:
            holoMemberTweet.holo_member_twitter_info = holoMemberTwitterInfo
            holoMemberTweet.holo_member_twitter_info_id = holoMemberTwitterInfo.twitter_id

    if "created_at" in tweet and tweet["created_at"]:
        holoMemberTweet.date = datetime.strptime(tweet["created_at"], "%a %b %d %X %z %Y").strftime('%Y-%m-%d %X')

    holoMemberTweet.tweet_id = tweet["id"]
    text = tweet["text"]

    entities = tweet["entities"]
    if "extended_tweet" in tweet:
        extend = tweet["extended_tweet"]
        text = extend["full_text"]
        if "user_mentions" in extend:
            entities["user_mentions"] = extend["user_mentions"]
        if "hashtags" in extend:
            entities["hashtags"] = extend["hashtags"]
        if "urls" in extend:
            entities["urls"] = extend["urls"]
        if "media" in extend:
            entities["media"] = extend["media"]

    if entities is not None and "user_mentions" in entities and entities["user_mentions"]:
        holoMemberTweet.user_mentions = list(set(map(lambda i: i["id"], entities["user_mentions"])))

    if entities is not None and "hashtags" in entities and entities["hashtags"]:
        holoMemberTweet.hashtags = list(set(map(lambda i: i["text"], entities["hashtags"])))

    if entities is not None and "urls" in entities and entities["urls"]:
        holoMemberTweet.urls = list(set(map(lambda i: i["expanded_url"], entities["urls"])))

    if entities is not None and "media" in entities and entities["media"]:
        holoMemberTweet.media = list(set(map(lambda i: i["media_url"], entities["media"])))

    holoMemberTweet.content = text

    if "retweeted_status" in tweet and "id" in tweet["retweeted_status"]:
        holoMemberTweet.rt_tweet_id = tweet["retweeted_status"]["id"]
        type = "RT"
    if "quoted_status" in tweet and "id" in tweet["quoted_status"]:
        holoMemberTweet.qt_tweet_id = tweet["quoted_status"]["id"]
        if type == "RT":
            type += "QT"
        else:
            type = "QT"

    if "BASE" == type and text[0] == "@" and "in_reply_to_status_id" in tweet:
        holoMemberTweet.reply_tweet_id = tweet["in_reply_to_status_id"]
        type = "REPLY"

    holoMemberTweet.type = type
    return holoMemberTweet


def __exit__(self):
    LOG.info("__exit__ START")
    db_session.delete_all(test_list)
    db_session.commit()
    db_session.close()
    LOG.info("__exit__ DB CLEAR")
    super.__exit__
