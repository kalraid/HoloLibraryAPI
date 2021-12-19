from datetime import datetime

import dateutil

import log
from app.database import get_session
from app.model import HoloMemberTweet, HoloMemberTwitterInfo, HoloMemberTwitterHashtag, HoloMemberTwitterMention, HoloMemberTwitterUrl, HoloMemberTwitterMedia

db_session = get_session()
test_list = list

LOG = log.get_logger()

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
        # holoMemberTweet.user_mentions =list(set(map(lambda i: i["id"], entities["user_mentions"])))
        mentions = []
        for i in entities["user_mentions"]:
            holoMemberTwitterMention = HoloMemberTwitterMention()
            holoMemberTwitterMention.holo_member_tweet_id = holoMemberTweet.tweet_id
            holoMemberTwitterMention.mention_id = i["id"]
            mentions.append(holoMemberTwitterMention)

        holoMemberTweet.holo_member_twitter_mention = mentions

    if entities is not None and "hashtags" in entities and entities["hashtags"]:
        #holoMemberTweet.hashtags = list(set(map(lambda i: i["text"], entities["hashtags"])))
        hashtags = []
        for i in entities["hashtags"]:
            holoMemberTwitterHashtag = HoloMemberTwitterHashtag()
            holoMemberTwitterHashtag.holo_member_tweet_id = holoMemberTweet.tweet_id
            holoMemberTwitterHashtag.hashtag = i["text"]
            hashtags.append(holoMemberTwitterMention)

        holoMemberTweet.holo_member_twitter_hashtag = hashtags

    if entities is not None and "urls" in entities and entities["urls"]:
        #holoMemberTweet.urls = list(set(map(lambda i: i["expanded_url"], entities["urls"])))
        urls = []
        for i in entities["urls"]:
            holoMemberTwitterUrl = HoloMemberTwitterUrl()
            holoMemberTwitterUrl.holo_member_tweet_id = holoMemberTweet.tweet_id
            holoMemberTwitterUrl.url = i["expanded_url"]
            urls.append(holoMemberTwitterMention)

        holoMemberTweet.holo_member_twitter_url = urls

    if entities is not None and "media" in entities and entities["media"]:
        #holoMemberTweet.media = list(set(map(lambda i: i["media_url"], entities["media"])))
        media = []
        for i in entities["urls"]:
            holoMemberTwitterMedia = HoloMemberTwitterMedia()
            holoMemberTwitterMedia.holo_member_tweet_id = holoMemberTweet.tweet_id
            holoMemberTwitterMedia.media_link = i["media_url"]
            media.append(holoMemberTwitterMention)

        holoMemberTweet.holo_member_twitter_media = media

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
