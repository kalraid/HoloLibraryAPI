twitter_consumer_key = "LyJRYgDOXyXgkEwVfCzZdvYZx"
twitter_consumer_secret = "GJqGw39xTKs63CQB84vvxuhAnLifVPIkeYHehNH7pypGwGqjoq"
#twitter_access_token = "AAAAAAAAAAAAAAAAAAAAAHsjTgEAAAAAWiB8zHi6GLqE1aF%2F4yNtd8kMqnQ%3DXBQE9cq3pSVn0PrT9ln4vmLyqsGNeuTAuril09anUvI1qifuUg"
twitter_access_token = "1433414457179312128-Rk4M7AhwcoOS5l4vGLHpGhZPU5RT6Y"
twitter_access_secret = "MOsBpp5QYq8lhwZXGdXsDNTrSftcAod7kAoPSRVC5f5hh"
import twitter
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret,
                          access_token_key=twitter_access_token,
                          access_token_secret=twitter_access_secret)


import json

account = ["880317891249188864","1433414457179312128"]
output_file_name = "stream_result.txt"
with open(output_file_name, "w", encoding="utf-8") as output_file:
    stream = twitter_api.GetStreamFilter(follow=account)   # GetStreamSample #GetUserStream
    while True:
        for tweets in stream:
            tweet = json.dumps(tweets, ensure_ascii=False)
            print(tweet, file=output_file, flush=True)