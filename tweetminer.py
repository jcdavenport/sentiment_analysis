#!/usr/bin/env python3

# examples:
# python tweetminer.py -q happy -s positive -t train -l 200
# python tweetminer.py -q happy -s positive -t test -l 20
# python tweetminer.py -q sad -s negative -t train -l 200
# python tweetminer.py -q sad -s negative -t test -l 20

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

    parser.add_argument("-t",
                        "--type",
                        dest="type",
                        help="type of file: train or test")

    parser.add_argument("-l",
                        "--limit",
                        dest="limit",
                        help="tweet collection limit '# of tweets'")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""
    def __init__(self, senti, query, f_type, t_limit):
        super().__init__()
        q_fname = query
        s_fname = senti
        t_fname = f_type

        self.counter = 0
        self.limit = t_limit

        self.outfile = "data/%s/mined/stream_%s_%s.json" % (s_fname, q_fname, t_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:

                if self.counter < self.limit:
                    f.write(data)
                    # print(data)
                    print("Tweets Collected: ", self.counter+1)
                    self.counter += 1
                    return True
                else:
                    handler()
                    return False

        except Exception as e:
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


def handler():
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


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    query_fname = format_filename(args.query)
    senti_fname = format_filename(args.senti)
    type_fname = format_filename(args.type)
    tweet_limit = int(args.limit)

    # prepare file names for modules
    input_file = "data/%s/mined/stream_%s_%s.json" % (senti_fname, query_fname, type_fname)
    output_file = "data/%s/mined/%s_%s_output.json" % (senti_fname, query_fname, type_fname)
    text_file = "data/%s/mined/%s2text_%s.txt" % (senti_fname, query_fname, type_fname)
    new_file = "data/%s/%s/%s_%ser.txt" % (senti_fname, type_fname, query_fname, type_fname)

    try:
        # start the data mining
        twitter_stream = Stream(auth, MyListener(senti_fname, query_fname, type_fname, tweet_limit))
        twitter_stream.filter(track=[args.query])
        # for mutliple filters: track=[args.query1, args.query2]

    # Listening for CTRL+C to stop data miner and either:
    # - continue to the processing phase, or
    # - exit the program
    except KeyboardInterrupt:
        handler()
    finally:
        sys.exit()
