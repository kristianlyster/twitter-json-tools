import json
from datetime import datetime


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
    # Se på datafelter i en tweet, og behold kun de ønskede feltene
    fields_to_remove = list(tweet.keys())
    for field in fields_to_keep:
        if field in fields_to_remove:
            fields_to_remove.remove(field)

    for field in fields_to_remove:
        del tweet[field]

    return tweet


def generate_tweet_link(tweet):
    return 'https://twitter.com/' + tweet['user'] + '/status/' + tweet['id']


apidateformat = '%a %b %d %H:%M:%S %z %Y'


def rearrange_tweet_data(tweet):
    tweet['user'] = tweet['user']['screen_name']
    tweet['id'] = tweet['id_str']

    tweet['created_at'] = datetime.strptime(tweet['created_at'], apidateformat)

    hashtags_dict = tweet['entities']['hashtags']
    hashtags = []
    for hashtag in hashtags_dict:
        hashtags.append(hashtag['text'])
    tweet['hashtags'] = hashtags

    mentions_dict = tweet['entities']['user_mentions']
    mentions = []
    for mention in mentions_dict:
        mentions.append(mention['screen_name'])
    tweet['mentions'] = mentions

    return tweet


def print_counter(counter, name='Element'):
    print('{0:20}Antall'.format(name))
    print('--------------------------')
    for elem in counter:
        print('{0:20}{1}'.format(elem[0] + ':', elem[1]))
