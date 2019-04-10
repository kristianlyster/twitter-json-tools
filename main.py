import json
from datetime import datetime
from collections import Counter


def name_to_filename(name):
    # Tar inn kandidatens twitter-navn og returnerer filnavnet til en .json-fil
    return name + '-tweets.json'


def read_tweets_from_file(filename):
    # Les inn tweets fra en gitt .json-fil
    tweets = []
    print('Laster fra fil:', filename)
    for line in open('json/' + filename):
        tweets.append(json.loads(line))

    return tweets


def mark_for_deletion_if_exists(tweets, field):
    # Finn tweets hvor gitte felter eksisterer,
    # og returner indeks til alle tweets som
    # matcher minst ett av kriteriene

    matches = []

    for index, tweet in enumerate(tweets):
        try:
            if tweet[field] and index not in matches:
                matches.append(index)
        except KeyError:
            pass

    return matches


def remove_excess_data(tweet, fields_to_keep):
    # Se på datafelter i entweet, og behold kun de ønskede feltene
    fields_to_remove = list(tweet.keys())
    for field in fields_to_keep:
        if field in fields_to_remove:
            fields_to_remove.remove(field)

    for field in fields_to_remove:
        del tweet[field]

    return tweet


def search_for_keyword_in_field(tweets, keyword, field):
    # Søk etter et stikkord i et sett med tweets
    # Returnerer antallet treff, og en liste med indeks til tweets med treff

    matches = []

    for index, tweet in enumerate(tweets):
        text = tweet[field]
        if keyword.lower() in text.lower().split():
            matches.append(index)

    return len(matches), matches


def search_for_word(tweets, word):
    # Snarvei for å søke i en liste med tweets etter et ord
    return search_for_keyword_in_field(tweets, word, 'full_text')


def search_for_hashtag(tweets, hashtag):
    # Snarvei for å søke i en liste med tweets etter en hashtag
    return search_for_keyword_in_field(tweets, hashtag, 'hashtags')


def search_for_mention(tweets, username):
    # Snarvei for å søke i en liste med tweets etter mentions av et @handle
    return search_for_keyword_in_field(tweets, username, 'mentions')


def get_list_of_matches(tweets, indexes):
    # Tar inn liste med indekser fra et søk
    # Returnerer listen indeksene refererer til
    result = []
    for index in indexes:
        result.append(tweets[index])

    return result


def get_sublist_containing_word(tweets, word):
    # Snarvei for å hente en liste med tweets som inneholder et søkeord
    _, indexes = search_for_word(tweets, word)
    return get_list_of_matches(tweets, indexes)


def get_sublist_containing_hashtag(tweets, hashtag):
    # Snarvei for å hente en liste med tweets som inneholder en hashtag
    _, indexes = search_for_hashtag(tweets, hashtag)
    return get_list_of_matches(tweets, indexes)


def get_sublist_containing_mention(tweets, username):
    # Snarvei for å hente en liste med tweets som nevner et @handle
    _, indexes = search_for_mention(tweets, username)
    return get_list_of_matches(tweets, indexes)


def generate_tweet_link(tweet):
    return 'https://twitter.com/' + tweet['user'] + '/status/' + tweet['id']


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
    tweet['user'] = tweet['user']['screen_name']
    tweet['id'] = tweet['id_str']

    hashtags_dict = tweet['entities']['hashtags']
    hashtags = ''
    for hashtag in hashtags_dict:
        hashtags += ' ' + hashtag['text']
    tweet['hashtags'] = hashtags

    mentions_dict = tweet['entities']['user_mentions']
    mentions = ''
    for mention in mentions_dict:
        mentions += ' ' + mention['screen_name']
    tweet['mentions'] = mentions

fields_to_keep = ['created_at', 'full_text', 'mentions',
                  'hashtags', 'id', 'user', 'favorite_count', 'retweet_count']

# FJERN UNYTTIGE DELER AV DATA

for tweet in tweets:
    tweet = remove_excess_data(tweet, fields_to_keep)

# SØK ETTER ORD, HASHTAG ELLER

# word = 'democracy'

# wordmatches, wordmatchindexes = search_for_word(tweets, word)

# print("Antall tweets med ordet", word, "i:", wordmatches)
# print("Eksempel på tweet med ordet", word + ":")
# print(generate_tweet_link(tweets[wordmatchindexes[0]]))
# print(tweets[wordmatchindexes[0]]['full_text'])
# print()

# hashtag = 'Brexit'

# hashtagmatches, hashtagmatchindexes = search_for_hashtag(tweets, hashtag)

# print("Antall tweets med hashtaggen", '#' + hashtag, "i:", hashtagmatches)
# print("Eksempel på tweet med hashtaggen", '#' + hashtag + ':')
# print(generate_tweet_link(tweets[hashtagmatchindexes[0]]))
# print(tweets[hashtagmatchindexes[0]]['full_text'])
# print()

# username = 'EPP'

# mentionmatches, mentionmatchindexes = search_for_mention(tweets, username)

# print("Antall tweets som nevner", '@' + username + ":", mentionmatches)
# print("Eksempel på tweet som nevner", '@' + username + ":")
# print(generate_tweet_link(tweets[mentionmatchindexes[0]]))
# print(tweets[mentionmatchindexes[0]]['full_text'])

# HVEM NEVNER #BREXIT MEST?

EPP_tweets = get_sublist_containing_word(tweets, 'UK')

print("Antall tweets som nevner UK:", len(EPP_tweets))

tweeters = [tweet['user'] for tweet in tweets]

print(Counter(tweeters).most_common())
