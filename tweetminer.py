#!/usr/bin/env python3

# To run this code, first edit config.py with your configuration, then:
# 1. IMPORTANT! Create a config.py file that contains your own Twitter
# API development credentials, i.e.:
# consumer_key = 'your_consumer_key'
# consumer_secret = 'your_consumer_key'
# access_token = 'your_access_token'
# access_secret = 'your_access_secret'
#
# 2. create a venv that uses python3.x, and install requirements.txt
#
# USE:
# 3. python tweetminer.py -q happy
# 4. python preprocess.py
# 5. python cleaner.py
#
# It will produce the list of tweets for the query "happy"
# in the file data/positive/stream_happy.json
#
# 6. Repeat steps 3-5 to process 'sad' data, i.e.:
# python tweetminer.py -q sad

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import nltk.downloader

print("Downloading nltk packages...")
nltk.download('punkt')
nltk.download('stopwords')
# nltk.download('tokenize')
print("DONE!\nNow launching Twitter live stream collector (CTRL+C to stop)...")
time.sleep(2)


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')

    # Directory argument is currently hardcoded!!
    # parser.add_argument("-d",
    #                     "--data-dir",
    #                     dest="data_dir",
    #                     help="Output/Data Directory")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    # def __init__(self, data_dir, query):
    def __init__(self, query):
        # hardcoded values for file locations
        if query == 'happy':
            data_dir = 'positive'
        else:
            data_dir = 'negative'

        query_fname = format_filename(query)
        self.outfile = "data/%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    # twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
    twitter_stream = Stream(auth, MyListener(args.query))
    twitter_stream.filter(track=[args.query])
