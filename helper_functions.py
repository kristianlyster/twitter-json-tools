import json


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


def generate_tweet_link(tweet):
    return 'https://twitter.com/' + tweet['user'] + '/status/' + tweet['id']
