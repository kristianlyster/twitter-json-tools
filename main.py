import json
from datetime import datetime
from collections import Counter
from textblob import TextBlob
# Imports helper functions from our own created files
from helper_functions import *
from search_functions import *

# SELECTIONS, FILES TO DOWNLOAD TWEETS FROM
candidates = ['BasEickhout', 'GuyVerhofstadt', 'ManfredWeber', 'SkaKeller',
              'TimmermansEU', 'Vestager', 'YanisVaroufakis', 'ZahradilJan']

# searchwords = ['EP2019', 'StrongerTogether', 'ItsTime', 'RetuneTheEU', LetsActTogether, 'RenewEurope', 'EuropeanSpring']

# DOWNLOADS TWEETS FROM JSON-FILES
tweets = []

for candidate in candidates:
    tweets.extend(read_tweets_from_file(name_to_filename(candidate)))
    
#for searchword in searchwords:
    #tweets.extend(read_tweets_from_file(name_to_filename(searchword)))

print("Tweets ferdig lastet!")
print()

# FILTERS IRRELEVANT DATA

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

# REARRANGE TWEETS IN ORDER TO GATHER USEFUL PARTS OF ['user'] AND ['entities'] 

for tweet in tweets:
    tweet = rearrange_tweet_data(tweet)


# REMOVE EXCESS DATA

fields_to_keep = ['created_at', 'full_text', 'mentions',
                  'hashtags', 'id', 'user', 'favorite_count', 'retweet_count',
                  'user_followers', 'interaction_rate']

for tweet in tweets:
    tweet = remove_excess_data(tweet, fields_to_keep)

####################################################

####Find Tweets with no retweets ###
#
#for i in tweets:
    #try:
        #if i['retweeted_status']:
            #tweets.remove(i)
    #except KeyError:
        #continue

#print("Antall tweets etter filtrering:", len(tweets))
#print()
#print("Tweeter uten retweets:")

#count = 0

#for tweet in tweets:
    #if tweet['retweet_count'] == 0:
        #count += 1
        #print("{}) Tweet fra {}:".format(count, tweet['user']['name']))
        #print("http://twitter.com/{}/status/{}".format(tweet['user']['screen_name'], tweet['id']))
        #print()

########### Sort tweets by favorite count or retweets #########

tweets = sort_list_by_value(tweets, 'favorite_count' #'retweet_count')

for i in range(10):
    print('{}: https://twitter.com/{}/status/{} med {} likes'.format(i + 1, tweets[i]['user'], tweets[i]['id'], tweets[i]['favorite_count']))
    #print('{}: https://twitter.com/{}/status/{} med {} retweets'.format(i + 1, tweets[i]['user'], tweets[i]['id'], tweets[i]['retweet_count']))

### SEARCH FOR KEYWORDS ###                            
                            
 search_terms = 'climate'
#
# wordresults = get_sublist_containing_word(tweets, search_terms)
# tagresults = get_sublist_containing_hashtag(tweets, search_terms)

# totalresults = wordresults

#for result in tagresults:
    # if result not in totalresults:
       #  totalresults.append(result)

#print(len(totalresults))

### SENTIMENT ANALYSIS   ###                            
                            
# total_polarity = 0
# total_subjectivity = 0
#
# for tweet in tweets:
#    blob = TextBlob(tweet['full_text'])
#    total_polarity += blob.sentiment.polarity
#    total_subjectivity += blob.sentiment.subjectivity
#
# mean_polarity = total_polarity / len(tweets)
# mean_subjectivity = total_subjectivity / len(tweets)
#
# print("Snitt-polaritet:", mean_polarity)
# print("Snitt-subjektivitet:", mean_subjectivity)
                                 
                            
#### FIND WEIGHTED INTERACTION RATE PER FOLLOWER ####                            
                            
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
