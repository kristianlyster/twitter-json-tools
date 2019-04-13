import json
from datetime import datetime
from collections import Counter
from textblob import TextBlob
# Importer hjelpefunksjoner fra egne filer
from helper_functions import *
from search_functions import *

# UTVALG, FILER Å LASTE JSON FRA
candidates = ['BasEickhout', 'GuyVerhofstadt', 'ManfredWeber', 'SkaKeller',
              'TimmermansEU', 'Vestager', 'YanisVaroufakis', 'ZahradilJan']

# LAST TWEETS FRA JSON-FIL
tweets = []

for candidate in candidates:
    tweets.extend(read_tweets_from_file(name_to_filename(candidate)))

print("Tweets ferdig lastet!")
print()

# FILTRER RELEVANT DATA

print("Antall tweets før filter:", len(tweets))

unwanted_fields = []  # ['retweeted_status']  # , 'in_reply_to_status_id']
todelete = []

print('Filtrerer bort tweets med:', unwanted_fields)

for field in unwanted_fields:
    todelete.extend(mark_for_deletion_if_exists(tweets, field))

todelete.sort(reverse=True)

for index in todelete:
    del tweets[index]  # SLETT ALLE TWEETS FUNNET VED TIDLIGERE KRITERIER

print("Antall tweets etter filter:", len(tweets))
print()

# OMFORM TWEETS FOR Å HENTE UT NYTTIGE DELER AV USER OG ENTITIES

for tweet in tweets:
    tweet = rearrange_tweet_data(tweet)


# FJERN UNYTTIGE DELER AV DATA

fields_to_keep = ['created_at', 'full_text', 'mentions',
                  'hashtags', 'id', 'user', 'favorite_count', 'retweet_count',
                  'user_followers']

for tweet in tweets:
    tweet = remove_excess_data(tweet, fields_to_keep)


# search_terms = 'climate'

# wordresults = get_sublist_containing_word(tweets, search_terms)
# tagresults = get_sublist_containing_hashtag(tweets, search_terms)

# totalresults = wordresults

# for result in tagresults:
#     if result not in totalresults:
#         totalresults.append(result)

# print(len(totalresults))

total_polarity = 0
total_subjectivity = 0

for tweet in tweets:
    blob = TextBlob(tweet['full_text'])
    total_polarity += blob.sentiment.polarity
    total_subjectivity += blob.sentiment.subjectivity

mean_polarity = total_polarity / len(tweets)
mean_subjectivity = total_subjectivity / len(tweets)

print("Snitt-polaritet:", mean_polarity)
print("Snitt-subjektivitet:", mean_subjectivity)

# tweets_by_user = {}

# for tweet in tweets:
#     user = tweet['user']
#     if user not in tweets_by_user.keys():
#         tweets_by_user[user] = []
#     tweets_by_user[user].append(tweet)

# followers = {}

# for user in tweets_by_user.keys():
#     followers[user] = tweets_by_user[user][0]['user_followers']

# interaction_rates = {}


# for user, usertweets in tweets_by_user.items():
#     user_followers = followers[user]
#     totalrate = 0
#     for tweet in usertweets:
#         totalrate += (tweet['retweet_count'] + tweet['favorite_count']) / user_followers
#     interaction_rates[user] = totalrate / len(usertweets)

# for name in sorted(interaction_rates, key=interaction_rates.get, reverse=True):
#     print('{0:17} {1:8.4f}\tmed {2} følgere'.format(name + ':', interaction_rates[name], followers[name]))
