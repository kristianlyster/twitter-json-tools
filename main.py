import json
from datetime import datetime
from collections import Counter
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

unwanted_fields = ['retweeted_status', 'in_reply_to_status_id']
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
                  'hashtags', 'id', 'user', 'favorite_count', 'retweet_count']

for tweet in tweets:
    tweet = remove_excess_data(tweet, fields_to_keep)


# HVEM NEVNER #BREXIT MEST? (Eksempel på søk og analyse av resultat)

EPP_tweets = get_sublist_containing_mention(tweets, 'EPP')

print("Antall tweets som nevner @EPP:", len(EPP_tweets))

tweeters = [tweet['user'] for tweet in EPP_tweets]

print(Counter(tweeters).most_common())
