from datetime import datetime

import dateutil

import log
from app.database import get_session
from app.model import HoloMemberTweet, HoloMemberTwitterInfo, HoloMemberTwitterHashtag, HoloMemberTwitterMention, \
    HoloMemberTwitterUrl, HoloMemberTwitterMedia

__name__ = "twitter_parser"
__version__ = "0.0.1"

db_session = get_session()
test_list = list

LOG = log.get_logger()


def tweet_parse(tweet, ban_tags) -> HoloMemberTweet:
    LOG.info(f'tweet_parse start')
    tweet_type = "BASE"
    holoMemberTweet = HoloMemberTweet()

    user = tweet["user"]
    if user["id"]:
        # tweet id 로 DB twitter 정보를 가져옴
        holoMemberTwitterInfo = HoloMemberTwitterInfo().find_by_twitter_info_id(db_session, user["id"])

        # 가져온 정보가 없는경우 종료
        if holoMemberTwitterInfo is None:
            return None

        # 가져온 정보가 있는경우 Tweet에 추가
        if holoMemberTwitterInfo:
            holoMemberTweet.holo_member_twitter_info = holoMemberTwitterInfo
            holoMemberTweet.holo_member_twitter_info_id = holoMemberTwitterInfo.twitter_id

    # 날짜 정보 추가
    if "created_at" in tweet and tweet["created_at"]:
        holoMemberTweet.date = datetime.strptime(tweet["created_at"], "%a %b %d %X %z %Y").strftime('%Y-%m-%d %X')

    holoMemberTweet.tweet_id = tweet["id"]
    text = tweet["text"]

    # 확장 정보가 있는경우 text,user_mentions,  hashtags, urls, media 보정
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

    # 트윗 맨션 ( 타 트윗 닉네임 호출시 ) 저장 -> 추후 멤버간 감정분석 기초 자료
    if entities is not None and "user_mentions" in entities and entities["user_mentions"]:
        mentions = []
        for i in entities["user_mentions"]:
            holoMemberTwitterMention = HoloMemberTwitterMention()
            holoMemberTwitterMention.holo_member_tweet_id = holoMemberTweet.tweet_id
            holoMemberTwitterMention.mention_user_id = i["id"]
            mentions.append(holoMemberTwitterMention)

        holoMemberTweet.holo_member_twitter_mention = mentions

    # 트윗의 해시태그 저장
    if entities is not None and "hashtags" in entities and entities["hashtags"]:
        hashtags = []
        for i in entities["hashtags"]:
            holoMemberTwitterHashtag = HoloMemberTwitterHashtag()
            holoMemberTwitterHashtag.holo_member_tweet_id = holoMemberTweet.tweet_id
            holoMemberTwitterHashtag.hashtag = "#" + i["text"]
            holoMemberTwitterHashtag.datatype = "tweet"
            holoMemberTwitterHashtag.tagtype = "test2"

            # 혹시라도 태그가 밴되있는 경우 태그 미사용으로 입력
            if i in ban_tags:
                holoMemberTwitterHashtag.isUse = "N"

            hashtags.append(holoMemberTwitterHashtag)

        holoMemberTweet.holo_member_twitter_hashtag = hashtags

    # 트위터 내부에 url이 적힌경우 저장
    if entities is not None and "urls" in entities and entities["urls"]:
        # holoMemberTweet.urls = list(set(map(lambda i: i["expanded_url"], entities["urls"])))
        urls = []
        for i in entities["urls"]:
            holoMemberTwitterUrl = HoloMemberTwitterUrl()
            holoMemberTwitterUrl.holo_member_tweet_id = holoMemberTweet.tweet_id
            holoMemberTwitterUrl.url = i["expanded_url"]
            urls.append(holoMemberTwitterUrl)

        holoMemberTweet.holo_member_twitter_url = urls

    # 트위터 내부 이미지, 외부 비디오, 기타 비디오, 기타 등등 에대해서 트윗에 삽입된경우 처리해줌
    # 즉 holoMemberTwitterMedia 의 media_typ = 'img' 인 경우가 멤버가 사진을 올린경우 <- 팬아트라는 보장은 없음
    # ext_video, ot_video 인경우 그대로 입력이 아니라 변환해서 처리
    # ex  (poster="https://pbs.twimg.com/tweet_video_thumb/FRYWXUgWQAA0SbW.jpg" src="https://video.twimg.com/tweet_video/FRYWXUgWQAA0SbW.mp4" type="video/mp4")
    if entities is not None and "media" in entities and entities["media"]:
        # holoMemberTweet.media = list(set(map(lambda i: i["media_url"], entities["media"])))
        media = []
        for i in entities["media"]:
            holoMemberTwitterMedia = HoloMemberTwitterMedia()
            holoMemberTwitterMedia.holo_member_tweet_id = holoMemberTweet.tweet_id
            media_url = i["media_url"]
            if 'media' in media_url:
                holoMemberTwitterMedia.media_type = 'img'
            elif 'ext_tw_video_thumb' in media_url:
                holoMemberTwitterMedia.media_type = 'ext_video'
            elif '_video_thumb' in media_url:
                holoMemberTwitterMedia.media_type = 'ot_video'
            else:
                holoMemberTwitterMedia.media_type = 'other'

            holoMemberTwitterMedia.media_link = media_url
            media.append(holoMemberTwitterMedia)

        holoMemberTweet.holo_member_twitter_media = media

    # text가 요약, 풀텍스트 두종류 이므로 풀텍스트를 저장
    holoMemberTweet.content = text

    # 트윗 타입 지정 RT - 리트윗, QT - 인용
    if "retweeted_status" in tweet and "id" in tweet["retweeted_status"]:
        holoMemberTweet.rt_tweet_id = tweet["retweeted_status"]["id"]
        tweet_type = "RT"
    if "quoted_status" in tweet and "id" in tweet["quoted_status"]:
        holoMemberTweet.qt_tweet_id = tweet["quoted_status"]["id"]
        if tweet_type == "RT":
            tweet_type += "QT"
        else:
            tweet_type = "QT"

    # 해당부분 재검토 필요 현재, RT, QT RTQT, BASE, REPLY 각각 존재
    if "BASE" == tweet_type and text[0] == "@" and "in_reply_to_status_id" in tweet:
        holoMemberTweet.reply_tweet_id = tweet["in_reply_to_status_id"]
        tweet_type = "REPLY"

    holoMemberTweet.tweet_type = tweet_type
    holoMemberTweet.holo_member_twitter_hashtag
    return holoMemberTweet
