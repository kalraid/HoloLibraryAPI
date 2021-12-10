import log

import twitter_test
from app.database import get_session
from app.model import HoloMemberTwitterInfo

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
output_file_name = "stream_result.txt"
db_session = get_session()
test_list = []
LOG = log.get_logger()

with open(output_file_name, "w", encoding="utf-8") as output_file:
    account = HoloMemberTwitterInfo().get_twitter_ids(db_session)
    stream = twitter_api.GetStreamFilter(follow=account, filter_level="low")  # GetStreamSample #GetUserStream
    twitter_api.GetUserStream()
    while True:
        for tweets in stream:
            if "user" in tweets and "id" in tweets["user"]:
                twitter_id = str(tweets["user"]["id"])
                if twitter_id in account:
                    index = account.index(twitter_id)
                    tweet = json.dumps(tweets, ensure_ascii=False)
                    print(tweet, file=output_file, flush=True)
                    tweet_parse_result = twitter_test.tweet_parse(twitter_test, tweets)
                    # LOG.info("tweet_parse_result : {}".format(tweet_parse_result))
                    if tweet_parse_result:
                        db_session.add(tweet_parse_result)
                        # test_list.append({tweet_parse_result})
                        db_session.commit()
