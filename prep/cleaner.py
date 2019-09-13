#!/usr/bin/env python3

__author__ = 'Joshua Davenport'
__license__ = 'MIT'
__email__ = 'jxdx_dev@protonmail.com'

import os
import re
import nltk

from nltk import word_tokenize

# ######## ONLY MODIFY THESE 2 VARIABLES! #########

# file = '../data/positive/happy2text.txt'
# file = 'data/negative/sad2text.txt'

# newfile = '../data/positive/train/happy_trainer.txt'
# newfile = 'data/negative/train/sad_trainer.txt'

# ############# END OF MODIFICATIONS ##############


words = set(nltk.corpus.words.words())
# tempfile = '\.tmp.txt'


def clean(txt_file, n_file):
    # txt_file1 = '../'+txt_file
    # n_file1 = '../'+n_file

    # FOR TESTING #
    # inp = input("TESTING: enter '0' to exit: ")
    #
    # if int(inp) is 0:
    #     print("Goodbye!")
    #
    #     # for testing
    #     print("txt_file1 = " + txt_file1)
    #     print("n_file1 = " + n_file1)
    #
    #     exit()
    # else:
    #     # exit no matter what user enters
    #     exit()
    # END TEST #

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

                # checking for duplicate lines (only checks adjacent duplicates)
                if text2 != text1:
                    op.write(' '.join([w.lower() for w in word_tokenize(text1)]) + '\n')
                    text2 = text1
    # os.remove(tempfile)
    return


# if __name__ == '__main__':
#     print("Cleaning the processed data...")
#     clean(file)
#     print("DONE!")
