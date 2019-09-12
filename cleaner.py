#!/usr/bin/env python3

__author__ = 'Joshua Davenport'
__license__ = 'MIT'
__email__ = 'jxdx_dev@protonmail.com'

import os
import re
import nltk

from nltk import word_tokenize

# ######## ONLY MODIFY THESE 2 VARIABLES! #########

file = 'data/positive/happy2text.txt'
# file = 'data/negative/sad2text.txt'

newfile = 'data/positive/train/happy_trainer.txt'
# newfile = 'data/negative/train/sad_trainer.txt'

# ############# END OF MODIFICATIONS ##############


words = set(nltk.corpus.words.words())
tempfile = 'data/.tmp.txt'


def clean(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename, 'r') as infile:
        lines = infile.readlines()

    with open(filename, 'w') as outfile:
        lines = filter(lambda x: x.strip(), lines)
        outfile.writelines(lines)

    with open(filename, 'r') as infile, \
            open(tempfile, 'w') as outfile:
        data = infile.read()

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
        outfile.write(data.strip())

        # finally, remove any stubborn blank lines
        with open(tempfile, 'r') as ip, \
                open(newfile, 'w') as op:
            fdata = ip.readlines()
            text2 = ''
            for li in fdata:
                if len(li) > 6:
                    text1 = li.lstrip()
                    # checking for duplicate lines (only checks adjacent duplicates)
                    if text2 != text1:
                        op.write(' '.join([w.lower() for w in word_tokenize(text1)]) + '\n')
                        text2 = text1
        os.remove(tempfile)


if __name__ == '__main__':
    clean(file)
