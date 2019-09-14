#!/usr/bin/env python3

__author__ = 'Joshua Davenport'
__license__ = 'MIT'
__email__ = 'jxdx_dev@protonmail.com'

import os
import re
import nltk

from nltk import word_tokenize

words = set(nltk.corpus.words.words())


#######################################################
# [Cleaning the text file]                            #
# Uses multiple passes to perform additional stemming #
# and removal of undesired whitespace.                #
#######################################################
def clean(txt_file, n_file):

    if not os.path.isfile(txt_file):
        print("{} does not exist ".format(txt_file))
        return

    ##########
    # pass 1 #
    ##########
    with open(txt_file, 'r') as inf:
        lines = inf.readlines()
    with open(txt_file, 'w') as outf:
        lines = filter(lambda x: x.strip(), lines)
        outf.writelines(lines)

    ##########
    # pass 2 #
    ##########
    with open(txt_file, 'r') as inf:
        data = inf.read()
    with open(n_file, 'w') as outf:
        # clean it up a bit. some of these are probably not needed.
        data = re.sub(r'RT @[_A-Za-z0-9]+: ', '', data)
        data = data.replace(':', '')
        data = data.replace(': ', '')
        data = data.replace(' :', '')
        data = re.sub(r'\d+', '', data)
        data = re.sub(r'[^\w\s]', '', data)
        data = data.strip()

        # remove non-English words
        " ".join(w for w in nltk.wordpunct_tokenize(data)
                 if w.lower() in words or not w.isalpha())

        outf.write(data.strip())

    ###########################################
    # pass 3, remove any stubborn blank lines #
    ###########################################
    with open(n_file, 'r') as ip:
        fdata = ip.readlines()
        text2 = ''
    with open(n_file, 'w') as op:
        for li in fdata:
            if len(li) > 6:
                text1 = li.lstrip()

                # TODO:
                #  Create function to check for any duplicates in fext file

                # checking for duplicate lines (only checks adjacent duplicates)
                if text2 != text1:
                    op.write(' '.join([w.lower() for w in word_tokenize(text1)]) + '\n')
                    text2 = text1
    return
