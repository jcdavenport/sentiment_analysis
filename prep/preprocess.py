#!/usr/bin/env python3

import json
import os
from os import path
from prep.pyTweetCleaner import TweetCleaner


####################################################
# [Converts processed .json to .txt file]          #
# Since all we care about in the .json file is the #
# actual text, why not put it into .txt format?    #
####################################################
def to_text(ofile, tfile):

    if path.exists(tfile):
        os.remove(tfile)
    with open(ofile, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            with open(tfile, 'a') as txt:
                txt.writelines(tweet['text'] + '\n')
    return


##########################################
# [Sends raw data to initial processing] #
##########################################
def tcleaner(in_file, out_file, txt_file):

    tc = TweetCleaner(remove_stop_words=True, remove_retweets=False)
    tc.clean_tweets(in_file, out_file)
    to_text(out_file, txt_file)

    return
