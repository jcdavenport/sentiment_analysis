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

# TODO:
#  Add option to specify limit on lines of data to collect.

# TODO:
#  Add option to import a previously captured .json file for processing.

# TODO:
#  Add option to collect and store data in a database.

# TODO:
#  Add a multithreaded process to run (and stop)
#  the stream data miner, and process files
#  simultaneously.

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import sys
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
    def __init__(self, senti, query):
        q_fname = query
        s_fname = senti

        self.outfile = "data/%s/mined/stream_%s.json" % (s_fname, q_fname)

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
# end of MyListener class


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
    input_file = "data/%s/mined/stream_%s.json" % (senti_fname, query_fname)
    output_file = "data/%s/mined/%s_output.json" % (senti_fname, query_fname)
    text_file = "data/%s/mined/%s2text.txt" % (senti_fname, query_fname)
    new_file = "data/%s/train/%s_trainer.txt" % (senti_fname, query_fname)

    try:
        # start the data mining
        twitter_stream = Stream(auth, MyListener(senti_fname, query_fname))
        twitter_stream.filter(track=[args.query])

    # Listening for CTRL+C to stop data miner and either:
    # - continue to the processing phase, or
    # - exit the program
    except KeyboardInterrupt:
        ans = input("\nData mining has been stopped!\n\nWhat would you like to do?\n"
                    "(Enter '1' to process data, or '0' to exit): ")
        if int(ans) is 1:
            # process the data
            try:
                print("\nProcessing the collected data...")
                preprocess.tcleaner(input_file, output_file, text_file)
                time.sleep(2)
                print("DONE!")
                time.sleep(1)
            except BaseException as e:
                print("Error on_data: %s" % str(e))

            # clean the data
            try:
                print("\nCleaning the processed data...")
                cleaner.clean(text_file, new_file)
                time.sleep(2)
                print("DONE!")
                time.sleep(1)

            except BaseException as e:
                print("Error on_data: %s" % str(e))

            print("\nThe training file can be found in '" + new_file + "'")
            sys.exit()
        else:
            print("Goodbye!")
            sys.exit()
