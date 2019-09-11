#!/usr/bin/env python3

import json
import os
from os import path
from pyTweetCleaner import TweetCleaner


# ########### ONLY MODIFY THESE 3 VARIABLES! ############
# specify the location of your tweetminer.py output file:
# (Comment/Uncomment file names accordingly)
input_file = 'data/positive/stream_happy.json'
# input_file = 'data/negative/stream_sad.json'

output_file = 'data/positive/happy_output.json'
# output_file = 'data/negative/sad_output.json'

textfile = 'data/positive/happy2text.txt'
# textfile = 'data/negative/sad2text.txt'

# ################ END OF MODIFICATIONS #################


def to_text():
    if path.exists(textfile):
        os.remove(textfile)
    with open(output_file, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            # print(tweet['text'])
            with open(textfile, 'a') as txt:
                txt.writelines(tweet['text'] + '\n')


tc = TweetCleaner(remove_stop_words=True, remove_retweets=False)
tc.clean_tweets(input_file, output_file)
to_text()
