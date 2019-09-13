#!/usr/bin/env python3

import json
import os
from os import path
from prep.pyTweetCleaner import TweetCleaner


# ########### ONLY MODIFY THESE 3 VARIABLES! ############
# specify the location of your tweetminer.py output file:
# (Comment/Uncomment file names accordingly)
# input_file = '../data/positive/stream_happy.json'
# input_file = 'data/negative/stream_sad.json'

# output_file = '../data/positive/happy_output.json'
# output_file = 'data/negative/sad_output.json'

# textfile = '../data/positive/happy2text.txt'
# textfile = 'data/negative/sad2text.txt'

# ################ END OF MODIFICATIONS #################


def to_text(ofile, tfile):
    if path.exists(tfile):
        os.remove(tfile)
    with open(ofile, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            # print(tweet['text'])
            with open(tfile, 'a') as txt:
                txt.writelines(tweet['text'] + '\n')
    return


def tcleaner(in_file, out_file, txt_file):
    # in_file1 = '../' + in_file
    # out_file1 = '../' + out_file
    # txt_file1 = '../' + txt_file

    tc = TweetCleaner(remove_stop_words=True, remove_retweets=False)
    tc.clean_tweets(in_file, out_file)
    to_text(out_file, txt_file)

    return


# if __name__ == '__main__':
#     tcleaner()
