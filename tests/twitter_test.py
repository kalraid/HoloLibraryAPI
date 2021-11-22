twitter_consumer_key = ""
twitter_consumer_secret = ""
twitter_access_token = ""
twitter_access_secret = ""
import twitter
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret,
                          access_token_key=twitter_access_token,
                          access_token_secret=twitter_access_secret)


account = "@TheBlueHouseKR"
statuses = twitter_api.GetUserTimeline(screen_name=account, count=200, include_rts=True, exclude_replies=False)
print(statuses)

for status in statuses:
    print(status.text)
#     print(status.text.encode('utf-8'))

output_file_name = "twitter_get_timeline_result.txt"
with open(output_file_name, "w", encoding="utf-8") as output_file:
    for status in statuses:
        print(status, file=output_file)

query = "코로나"
statuses = twitter_api.GetSearch(term=query, count=100)
for status in statuses:
    print(status.text)


query = "#nthroom"
statuses = twitter_api.GetSearch(term=query, count=100)
for status in statuses:
    for tag in status.hashtags:
        print(tag.text)

from collections import Counter

query = "#nthroom"
statuses = twitter_api.GetSearch(term=query, count=100)
result = []
for status in statuses:
    for tag in status.hashtags:
        result.append(tag.text)

Counter(result).most_common(20)


import json
query = ["n번방"]
output_file_name = "stream_result.txt"
with open(output_file_name, "w", encoding="utf-8") as output_file:
    stream = twitter_api.GetStreamFilter(track=query)
    while True:
        for tweets in stream:
            tweet = json.dumps(tweets, ensure_ascii=False)
            print(tweet, file=output_file, flush=True)