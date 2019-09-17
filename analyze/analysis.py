"""
An implementation of the Twitter analysis tool mentioned on
http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/

happy.txt contains 80 tweets that are happy (positive),
sad.txt contains 80 tweets that are sad (negative).

happy_test.txt and sad_test.txt contains 10 positive
and 10 negative tweets respectively to test the
classifier.
"""
import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier

tweets = []


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def read_tweets(fname, t_type):
    tweets = []
    f = open(fname, 'r')
    line = f.readline()
    while line != '':
        tweets.append([line, t_type])
        line = f.readline()
    f.close()
    return tweets


def extract_features(document):
    document_words = set(document)
    features = {}
    # extract the word features out from the training data
    word_features = get_word_features(get_words_in_tweets(tweets))
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def classify_tweet(tweet, classifier):
    return classifier.classify(extract_features(nltk.word_tokenize(tweet)))


def analyze_data(pos_train, neg_train, pos_test, neg_test):
    global tweets

    pos_tweets = read_tweets(pos_train, 'positive')
    neg_tweets = read_tweets(neg_train, 'negative')

    # filter away words that are less than 3 letters to form the training data
    for (words, sentiment) in pos_tweets + neg_tweets:
        words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
        tweets.append((words_filtered, sentiment))

    # get the training set and train the Naive Bayes Classifier
    training_set = nltk.classify.util.apply_features(extract_features, tweets)
    classifier = NaiveBayesClassifier.train(training_set)

    # read in the test tweets and check accuracy
    # to add your own test tweets, add them in the respective files
    test_tweets = read_tweets(pos_test, 'positive')
    test_tweets.extend(read_tweets(neg_test, 'negative'))
    total = accuracy = float(len(test_tweets))

    for tweet in test_tweets:
        if classify_tweet(tweet[0], classifier) != tweet[1]:
            accuracy -= 1
    tot_accuracy = accuracy / total * 100

    print("\n\nResults:")
    print("######################################")
    print("## Total accuracy: ", end="")
    print('%.3f' % tot_accuracy, end="")
    print("%", end="")
    print(' (%d/%d)! ##' % (accuracy, total))
    print("######################################")
