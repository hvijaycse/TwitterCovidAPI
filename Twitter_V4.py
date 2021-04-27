from TwitterSearch import *
import os


ts = TwitterSearch(
    consumer_key=os.environ.get('consumer_key', None),
    consumer_secret=os.environ.get('consumer_secret', None),
    access_token=os.environ.get('access_token', None),
    access_token_secret=os.environ.get('access_token_secret', None),
)


def filterTweets(tso: TwitterSearchOrder, stopWords: list = None) -> list:
    '''
    This method takes two arguments TwitterSearchOrder
    objects and stopWords. It returns list of all 
    the tweets after filtering them for retweet and 
    stopWords.

    Args:
        tso : TwitterSearchOrder
        stopWords : list[str]

    return : list
    '''

    # Creating empty list
    tweetList = []

    if stopWords == None:
        stopWords = ['need', 'any ', 'require']

    filterCount = 0
    # Loop to filter tweets
    for tweet in ts.search_tweets_iterable(tso):
        # Condition for filtering tweet
        if "RT" not in tweet['full_text'][:3] and not any(word in tweet['full_text'].lower() for word in stopWords):
            # adding filtered tweet to list
            tweetList.append(tweet)
    return tweetList


def printTweets(ResourceName, tweetsList, ResultLimit=None):
    '''
    This method takes ResourceName, tweetsList and
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
        print("_" * 60)
        print()
        print(f"{tweet['user']['screen_name']}:")
        for line in tweet["full_text"].split("\n"):
            print(f"\t{line}")

    print(f"Tweet Fetched: {len(tweetsList)}")
    print('='*40)  # ending line
    print()  # empty line


def getResourceTSO(keywords: list, resultType: str = 'recent') -> list:
    '''
    This method takes two arguments keywords
    and resultType (optional).
    It creates a TwitterSearchOrder
    with keywords and with all the
    default parameteres required
    and return it..

    Args :
        keywords : list
        resultType : str
    return : TwitterSearchOrder
    '''
    tso = TwitterSearchOrder()
    tso.set_keywords(keywords)
    tso.set_result_type(result_type=resultType)
    tso.arguments.update({'tweet_mode': 'extended'})

    return tso


def getResourceTweets(keywords: list, stopWords: list = None):
    '''
    This method takes two arguments 
    keyowords list and stopwords list.
    It return list of tweets for 
    keywords by removing tweets with stopwords.

    Args :
        keywords : list[str]
        stopWords : list[str]

    return : list[dict]

    '''

    ResouceTSO = getResourceTSO(keywords)

    return filterTweets(ResouceTSO, stopWords)


if __name__ == "__main__":

    city = "jaipur"

    # REMDESIVIR FETCH
    remdesivirKeywords = ["remdesivir", "verified", city]
    # printTweets("REMDESIVIR", getResourceTweets(remdesivirKeywords))

    # FOOD FETCH
    foodKeywords = ["food", "covid", city]
    # printTweets("FOOD", getResourceTweets(foodKeywords, stopWords=[]))

    # OXYGEN BED FETCH
    oxygenBedKeywords = ["oxygen", "bed", "verified", city]
    # printTweets("OXYGEN BED", getResourceTweets(oxygenBedKeywords))

    # OXYGEN CYLINDER FETCH
    oxygenCylinderKeywords = ["Oxygen", "cylinder", "verified", city]
    # printTweets("OXYGEN CYLINDER", getResourceTweets(oxygenCylinderKeywords))

    # HOSPITAL BED FETCH
    hospitalBedKeywords = ["bed", "verified", city]
    # printTweets("HOSPITAL BEDS", getResourceTweets(hospitalBedKeywords))

    # ICU FETCH
    ICUKeywords = ["ICU", "verified", city]
    # printTweets("ICU", getResourceTweets(ICUKeywords))

    # NEWS FETCH
    NEWSKeywords = ["News", "covid", city]
    # printTweets("NEWS", getResourceTweets(NEWSKeywords))

    # TOCILIZUMAB FETCH
    TOCILIZUMABKeywords = ["Tocilizumab", "verified", city]
    # printTweets("TOCILIZUMAB", getResourceTweets(TOCILIZUMABKeywords))
