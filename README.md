# twitter-json-tools
A small set of functions and scripts intended to make processing and performing analysis on Twitter API JSON data easier.
The example script assumes JSON files with names in the format `username-tweets.json` are placed in a /json directory.
These JSON files should be multiline, with each line containing a JSON Tweet object as [defined in the Twitter API documentation](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html).

## Usage
For the most basic uses, modifying and/or appending to the included `main.py` should be plenty. 

## Requirements
These functions and scripts are based only on the core Python libraries. Only tested on python 3.6.4, but should work on any `python>=3`
