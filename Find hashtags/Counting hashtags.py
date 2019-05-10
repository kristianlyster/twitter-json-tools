import json
from collections import Counter
from helper_functions import *

tweets = []

for line in open('ManfredWeber-tweets.json'):
    tweets.append(json.loads(line))

print ("number of tweets before filtering", len(tweets))

unwanted_fields = ['retweeted_status'] # 'in_reply_to_status_id']
todelete = []

print('Filtering tweets with:', unwanted_fields)

for field in unwanted_fields:
    todelete.extend(mark_for_deletion_if_exists(tweets, field))

todelete.sort(reverse=True)

for index in todelete:
    del tweets[index]  # SLETT ALLE TWEETS FUNNET VED TIDLIGERE KRITERIER

print("number of tweets after filtering", len (tweets))

hashtags = []

for tweet in tweets:
    if 'entities' in tweet:
        hashtags.extend(tweet['entities']['hashtags'])

hashtags = [tag['text'].lower() for tag in hashtags]

hashtags = Counter(hashtags).most_common()[:10]

print (hashtags)