#!/usr/bin/env python3

# run:
# python tweetminer.py

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
#  Update README for main menu changes.

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
import string
import config
import json
import sys
import nltk.downloader
# import argparse

from prep import preprocess, cleaner

print("Downloading nltk packages...")
nltk.download('punkt')
nltk.download('words')
nltk.download('stopwords')
print("DONE!\nNow launching program menu...")
time.sleep(2)

input_file = ""
output_file = ""
text_file = ""
new_file = ""


def authority():
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    tweepy.API(auth)
    return auth


def menu():
    print()
    print("************MAIN MENU**************")
    # time.sleep(1)
    print()

    choice = input("""
    A: Create Training Data Set
    B: Create Testing Data Set
    C: Analyze Data
    Q: Quit

    Please enter your choice: """)

    if choice == "A" or choice == "a":
        trainer()
    elif choice == "B" or choice == "b":
        tester()
    elif choice == "C" or choice == "c":
        analyze()
    elif choice == "Q" or choice == "q":
        quitter()
    else:
        print("You must only select either A,B,C, or Q.")
        print("Please try again")
        menu()


def trainer():
    print("\n************Create Training Data Set**************")
    try:
        query_fname = input("\nWhat sentiment keyword would you like to set as the filter?: ")
        q_name = format_filename(query_fname)
    except IOError as e:
        print("Error on_data: %s" % str(e))

    try:
        senti_fname = input("What is the nature of this sentiment(1=Positive, 2=Negative)?: ")
        if int(senti_fname) is 1:
            se_name = "positive"
        elif int(senti_fname) is 2:
            se_name = "negative"
        else:
            print("Only select 1 or 2, genius!")
            trainer()
        s_name = format_filename(se_name)
    except IOError as e:
        print("Error on_data: %s" % str(e))

    try:
        type_fname = "train"
        t_name = format_filename(type_fname)
    except IOError as e:
        print("Error on_data: %s" % str(e))

    try:
        tweet_limit = input("How many tweets should be collected?(1-1000): ")
        if 1000 > int(tweet_limit) > 0:
            tw_limit = int(tweet_limit)
        elif int(tweet_limit) > 1000:
            # set to max limit
            tw_limit = 1000
        elif int(tweet_limit) < 0:
            tw_limit = 100
        else:
            print("Next time try an integer 1-1000!")
            trainer()

        t_limit = tw_limit
    except IOError as e:
        print("Error on_data: %s" % str(e))

    print()
    print("Query(Filter): ", q_name)
    print("Sentiment:     ", s_name)
    print("Type:          ", t_name)
    print("Tweet Limit:   ", t_limit)

    proceed = input("\nIs the above correct?(Y or N): ")
    if proceed == "N" or proceed == "n":
        print("resetting...")
        time.sleep(3)
        trainer()
    else:
        print("Initializing tweet capture...")
        time.sleep(2)
        file_ops(s_name, q_name, t_name)
        print("GO!!!")

    try:
        # start the data mining
        twitter_stream = Stream(authority(), MyListener(s_name, q_name, t_name, t_limit))
        twitter_stream.filter(track=[q_name])
        # for mutliple filters: track=[args.query1, args.query2]

    # Listening for CTRL+C to stop data miner and either:
    # - continue to the processing phase, or
    # - exit the program
    except KeyboardInterrupt:
        handler()


def tester():
    print("\n************Create Testing Data Set**************")
    try:
        query_fname = input("\nWhat sentiment keyword would you like to set as the filter?: ")
        # need some sort of input validation here
        q_name = format_filename(query_fname)
    except IOError as e:
        print("Error on_data: %s" % str(e))

    try:
        senti_fname = input("What is the nature of this sentiment(1=Positive, 2=Negative)?: ")
        if int(senti_fname) is 1:
            se_name = "positive"
        elif int(senti_fname) is 2:
            se_name = "negative"
        else:
            print("Only select 1 or 2, genius!")
            tester()
        s_name = format_filename(se_name)
    except IOError as e:
        print("Error on_data: %s" % str(e))

    try:
        type_fname = "test"
        t_name = format_filename(type_fname)
    except IOError as e:
        print("Error on_data: %s" % str(e))

    try:
        tweet_limit = input("How many tweets should be collected?(1-1000): ")
        if 1000 > int(tweet_limit) > 0:
            tw_limit = int(tweet_limit)
        elif int(tweet_limit) > 1000:
            # set to max limit
            tw_limit = 1000
        elif int(tweet_limit) < 0:
            tw_limit = 100
        else:
            print("Next time try an integer 1-1000!")
            trainer()

        t_limit = tw_limit
    except IOError as e:
        print("Error on_data: %s" % str(e))

    # check if everything is correct
    print()
    print("Query(Filter): ", q_name)
    print("Sentiment:     ", s_name)
    print("Type:          ", t_name)
    print("Tweet Limit:   ", t_limit)

    proceed = input("\nIs the above correct?(Y or N): ")
    if proceed == "N" or proceed == "n":
        print("resetting...")
        time.sleep(3)
        tester()
    else:
        print("Initializing tweet capture...")
        time.sleep(2)
        file_ops(s_name, q_name, t_name)
        print("GO!!!")

    try:
        # start the data mining
        twitter_stream = Stream(authority(), MyListener(s_name, q_name, t_name, t_limit))
        twitter_stream.filter(track=[q_name])
        # for mutliple filters: track=[args.query1, args.query2]

    # Listening for CTRL+C to stop data miner and either:
    # - continue to the processing phase, or
    # - exit the program
    except KeyboardInterrupt:
        handler()


def analyze():
    # placeholder
    print("Analyze...")
    time.sleep(3)
    menu()


def quitter():
    q_ans = input("\nAre you sure you want to quit?(Y or N): ")
    if q_ans == "N" or q_ans == "n":
        menu()
    else:
        print("Goodbye!")
        sys.exit()


def file_ops(s_name, q_name, t_name):
    # prepare file names for modules
    global input_file
    global output_file
    global text_file
    global new_file
    input_file = "data/%s/mined/stream_%s_%s.json" % (s_name, q_name, t_name)
    output_file = "data/%s/mined/%s_%s_output.json" % (s_name, q_name, t_name)
    text_file = "data/%s/mined/%s2text_%s.txt" % (s_name, q_name, t_name)
    new_file = "data/%s/%s/%s_%ser.txt" % (s_name, t_name, q_name, t_name)
    return


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
                    print(data)
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
    ans = input("\nFinished or manually halted!\nWhat would you like to do?\n"
                "(Enter '1' to Process Data, or '0' to Main Menu): ")
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
        ender()
    else:
        menu()


def ender():
    nav = input("\nWhat would you like to do?\n(1=MainMenu, 0=Exit): ")
    if int(nav) is 1:
        menu()
    elif int(nav) is 0:
        sys.exit()
    else:
        print("Pick either 1 or 0!")
        ender()


if __name__ == '__main__':
    menu()
