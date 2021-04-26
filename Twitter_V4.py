# import json
from TwitterSearch import *
from boto.s3.connection import S3Connection
import os


ts = TwitterSearch(
    consumer_key=S3Connection(os.environ['S3_KEY'], os.environ['consumer_key']),
    consumer_secret=S3Connection(os.environ['S3_KEY'], os.environ['consumer_secret']),
    access_token=S3Connection(os.environ['S3_KEY'], os.environ['access_token']),
    access_token_secret=S3Connection(os.environ['S3_KEY'], os.environ['access_token_secret']),
)


def filterTweets(tso: TwitterSearchOrder) -> list:
    '''
    This method takes a TwitterSearchOrder
    objects argument and returns list of all 
    the tweets after filtering them for
    retweet, need and required.

    Args:
        tso : TwitterSearchOrder
    return : list
    '''

    # Creating empty list
    tweetList = []

    # Loop to filter tweets
    for tweet in ts.search_tweets_iterable(tso):
        # Condition for filtering tweet
        if "RT" not in tweet['text'] and "need" not in tweet["text"].lower() and 'required' not in tweet['text'].lower():
            # adding filtered tweet to list
            tweetList.append(tweet)

    return tweetList


def printTweets(ResourceName, tweetsList, ResultLimit=None):
    '''
    This methos takes ResourceName, tweetsList and
    ResultLimit arguments.

    It prints tweets in format.

    Args :
        ResourceName : str
        tso : TwitterSearchOrder
        ResultLimit : int
    return : None
    '''

    print(ResourceName)

    if ResultLimit:
        tweetsList = tweetsList[:ResultLimit]

    for tweet in tweetsList:
        if "RT" not in tweet['text'] and "need" not in tweet["text"].lower() and 'required' not in tweet['text'].lower():
            print("_" * 60)
            print()
            print(f"{tweet['user']['screen_name']}:")
            for line in tweet["text"].split("\n"):
                print(f"\t{line}")

    print(f"Tweet Fetched: {len(tweetsList)}")
    print('='*40)  # ending line
    print()  # empty line


def getResourceTweets(keywords: list, resultType: str = 'recent') -> list:
    '''
    This method takes two arguments keywords
    and resultType (optional).
    It creates a TwitterSearchOrder
    with keywors and returns list
    of tweeets after filtering them
    using filterTweets method.

    Args :
        keywords : list
        resultType : str
    return : list
    '''
    tso = TwitterSearchOrder()
    tso.set_keywords(keywords)
    tso.set_result_type(result_type=resultType)

    return filterTweets(tso)


if __name__ == "__main__":

    city = "jaipur"

    # REMDESIVIR FETCH
    remdesivirKeywords = ["remdesivir", "available", "verified", city]
    # printTweets("REMDESIVIR", getResourceTweets(remdesivirKeywords))

    # FOOD FETCH
    foodKeywords = ["food", "covid", city]
    printTweets("FOOD", getResourceTweets(["food", "covid", city]))

    # OXYGEN FETCH
    oxygenKeywords = ["food", "covid", city]
    # printTweets("OXYGEN", getResourceTweets(oxygenKeywords))

    # HOSPITAL BED FETCH
    hospitalBedKeywords = ["bed", "available",  "covid", city]
    # printTweets("hospitalBed", getResourceTweets(hospitalBedKeywords))

    # ICU FETCH
    ICUKeywords = ["ICU", "available", city]
    # printTweets("ICU", getResourceTweets(ICUKeywords))

    # NEWS FETCH
    NEWSKeywords = ["News", "covid", city]
    # printTweets("NEWS", getResourceTweets(NEWSKeywords))
