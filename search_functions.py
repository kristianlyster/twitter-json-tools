def search_for_keyword_in_field(tweets, keyword, field):
    # Søk etter et stikkord i et sett med tweets
    # Returnerer antallet treff, og en liste med indeks til tweets med treff

    matches = []

    for index, tweet in enumerate(tweets):
        text = tweet[field]
        if isinstance(text, str):
            if keyword.lower() in text.lower().split():
                matches.append(index)
        elif isinstance(text, list):
            if keyword.lower() in [word.lower() for word in text]:
                matches.append(index)

    return matches


def search_for_word(tweets, word):
    # Snarvei for å søke i en liste med tweets etter et ord
    return search_for_keyword_in_field(tweets, word, 'full_text')


def search_for_hashtag(tweets, hashtag):
    # Snarvei for å søke i en liste med tweets etter en hashtag
    return search_for_keyword_in_field(tweets, hashtag, 'hashtags')


def search_for_mention(tweets, username):
    # Snarvei for å søke i en liste med tweets etter mentions av et @handle
    return search_for_keyword_in_field(tweets, username, 'mentions')


def search_for_tweets_from_user(tweets, username):
    # Snarvei for å søke i en liste med tweets etter tweets fra en bruker
    return search_for_keyword_in_field(tweets, username, 'user')


def get_list_of_matches(tweets, indexes):
    # Tar inn liste med indekser fra et søk
    # Returnerer listen indeksene refererer til
    result = []
    for index in indexes:
        result.append(tweets[index])

    return result


def get_sublist_containing_word(tweets, word):
    # Snarvei for å hente en liste med tweets som inneholder et søkeord
    indexes = search_for_word(tweets, word)
    return get_list_of_matches(tweets, indexes)


def get_sublist_containing_hashtag(tweets, hashtag):
    # Snarvei for å hente en liste med tweets som inneholder en hashtag
    indexes = search_for_hashtag(tweets, hashtag)
    return get_list_of_matches(tweets, indexes)


def get_sublist_containing_mention(tweets, username):
    # Snarvei for å hente en liste med tweets som nevner et @handle
    indexes = search_for_mention(tweets, username)
    return get_list_of_matches(tweets, indexes)


def get_sublist_containing_tweets_from_user(tweets, username):
    # Snarvei for å hente tweets fra en spesifikk bruker
    indexes = search_for_tweets_from_user(tweets, username)
    return get_list_of_matches(tweets, indexes)


def sort_list_by_value(tweets, key, highest_first=True):
    return sorted(tweets, key=lambda x: x[key], descending=highest_first)
