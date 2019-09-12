#!/usr/bin/env python3

# Based on Marco Bonzanini's blog "Minig Twitter Data with Python":
# https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
#
# Modified with customized functions and
# tweaked for simplified execution by:
# Joshua Davenport (Systems Developer)
#
# For instructions on use, refer to the README.md at:
# https://github.com/jcdavenport/sentiment_analysis

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
nltk.download('words')
nltk.download('stopwords')
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
        query_fname = format_filename(query)

        # hardcoded values for file locations
        if query_fname == 'happy':
            data_dir = 'positive'
        else:
            data_dir = 'negative'

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
