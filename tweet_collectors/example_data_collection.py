# Example codes to collect data.


import database_for_seminar as database
from pytz import timezone
import datetime
import examples_for_seminar as e

LT = timezone('Europe/Berlin')


#
# Collecting tweets containing a word 'trump' between 2019-2-25, 2019-2-26
#


# First, we store tweets into JSON file.
q = {'since': '2019-2-25', 'until': '2019-2-26', 'result_type': 'recent'} # set up parameter
e.save_search_to_file('trump', **q)

# Second, we put the JSON file into our database.
# !!!NOTE: Before importing JSON, check whether you set correct database name!!!
e.import_json('search.json')


#
# Collecting tweets recently published from '@CDU'
#

# First, we store tweets into JSON file (#3200)
e.save_user_archive_to_file('CDU')


# Second, we put the JSON file into our database.
# !!!NOTE: Before importing JSON, check whether you set correct database name!!!
e.import_json('CDU-tweets.json')


#
# Collecting tweets containing a word 'Merkel' from Streaming API.
#

# First, we store tweets into JSON file
e.save_track_keywords('Merkel') # type [Ctrl]+C to stop.

# Scond, we put the JSON file into our database.
e.import_json('keywords_example.json')



#
# Quick check
#

# check number of tweets in the database:
database.Tweet.select().count()

# check number of users in the database:
database.User.select().count()


#
# Print results
#

start_date = LT.localize(datetime.datetime(2018, 11, 1, 0))
stop_date = LT.localize(datetime.datetime(2018,11,13,0))

e.export_total_counts(start_date=start_date,stop_date=stop_date)
e.export_keyword_counts("day", ["Umvolkung","CDU","AfD"], start_date, stop_date)
export_retweets_period(n=100, start_date=start_date,stop_date=stop_date,
                         filename="top_retweets_text_100.csv")






