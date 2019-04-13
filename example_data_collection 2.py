##################################### Before run this code ################################
# Here are the things you need to do before run this codes.
# 0. Prepare a project folder which is connected to Python interpreter with following conditions:
#   -Python version 3.6 with following packages:
#     peewee<3, pytz, requests, requests-oauthlib, progress, python-dateutil
# 1. You must put all the relevant files into the project folder DIRECTLY.
# 2. PUT your tokens into 'config.py' file.
###########################################################################################


from pytz import timezone
import datetime
import examples_for_seminar as e ##### <- all the functions are coming from here
import database_for_seminar as database ##### <- database

### Setting timezone
LT = timezone('Europe/Berlin')


#
# REST API 1 : Search tweets containing certain keyword
#

# In this example, we search tweeets containing word 'trump' from yesterday to today.

today = str(datetime.datetime.utcnow().date()) # format should be "YYYY-MM-DD"
yesterday = str(datetime.datetime.utcnow().date() - datetime.timedelta(days=1)) # format should be "YYYY-MM-DD"

# Set up parameters
q = {'since': yesterday, 'until': today, 'result_type': 'recent'}

# This function search tweets and store this into json file named 'search.json'.
e.save_search_to_file('trump', **q)


#
# REST API 2: Collecting tweets of a certain user.
#
# In this example, we collect tweets published by @realDonaldTrump.

# This function store tweets into JSON file, named 'realDonaldTrump-tweets.json'.(#3200)
e.save_user_archive_to_file('realDonaldTrump')



#
# STREAMING API
#

# In this example, we track 'trump' (and obama)

# this function just print streaming result.
e.track_keywords('trump') # when you want to stop, press [ctrl + c]
e.track_keywords(['trump','obama']) # tweets containing either 'election' or 'obama'

# this function store result into json file named 'keywords_example.json'
e.save_track_keywords('trump')



#
# Utilizing Database
#

#
# Store json files into a database
# Database structure please check file 'database_for_seminar'
# !!! NOTE !!! Please check whether you set correct database name (XXXX.db) in
# 'database_for_seminar' file.
#

# this function import your json file into a database.
e.import_json('search.json')
e.import_json('realDonaldTrump-tweets.json')
e.import_json('keywords_example.json')


#
# Example codes working with database
#

# check number of tweets in the database: ## It refers to table tweet, then it selects them all and counts the words.
database.Tweet.select().count()

# check number of users in the database: ## Counts the number of users. Select all of them and count number of rules.
database.User.select().count()


#
# Export some stats of the data in the database
#

# Setting start date and end date. ## LT is local time. You can also do start_date as yesterday and stop day as today for instance
start_date = LT.localize(datetime.datetime(2018, 11, 1, 0)) # 0 means the time. Twelwe o' clock
stop_date = LT.localize(datetime.datetime(2018,11,13,0))

# Export total counts per day into csv file
e.export_total_counts(start_date=start_date,stop_date=stop_date)

# Export keyword counts per day into csv file.
e.export_keyword_counts("day", ["Umvolkung","CDU","AfD"], start_date, stop_date)

# Export n number of top retweets during the period.
e.export_retweets_period(n=100, start_date=start_date,stop_date=stop_date,
                         filename="top_retweets_text_100.csv")



