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

from prep import preprocess, cleaner

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

    parser.add_argument("-s",
                        "--sentiment",
                        dest="senti",
                        help="positive/negative")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    # def __init__(self, query):
    def __init__(self, senti, query):
        q_fname = query
        s_fname = senti

        # hardcoded values for file locations
        # if query_fname is 'happy':
        #     data_dir = 'positive'
        #     self.outfile = "data/%s/stream_%s.json" % (data_dir, query_fname)
        # else:
        #     data_dir = 'negative'
        #     self.outfile = "data/%s/stream_%s.json" % (data_dir, query_fname)

        self.outfile = "data/%s/stream_%s.json" % (s_fname, q_fname)

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

    query_fname = format_filename(args.query)
    senti_fname = format_filename(args.senti)

    # prepare file names for modules
    input_file = "data/%s/stream_%s.json" % (senti_fname, query_fname)
    output_file = "data/%s/%s_output.json" % (senti_fname, query_fname)
    text_file = "data/%s/%s2text.txt" % (senti_fname, query_fname)
    new_file = "data/%s/%s_trainer.txt" % (senti_fname, query_fname)

    try:
        twitter_stream = Stream(auth, MyListener(senti_fname, query_fname))
        # twitter_stream = Stream(auth, MyListener(args.query))
        twitter_stream.filter(track=[args.query])
    except KeyboardInterrupt:
        ans = input("\nData mining has been stopped!\n"
                    "(Enter '0' to exit): ")
        if int(ans) is 0:
            print("Goodbye!")

            # for testing
            print("input_file = " + input_file)
            print("output_file = " + output_file)
            print("text_file = " + text_file)
            print("new_file = " + new_file)

            exit()
        else:
            # exit no matter what user enters
            exit()

        # USED IN NEXT VERSION
        # ans = 1
        # ans = input("\nData mining has been stopped!\n\nWhat would you like to do?\n"
        #             "(Enter '1' to process data, or '0' to exit)[1]: ")
        # if ans == 0:
        #     print("Goodbye!")
        #     exit()
        # else:
        #     preprocess.tcleaner()
