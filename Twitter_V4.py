from TwitterSearch import *
import os
from datetime import datetime
from pytz import timezone

ts = TwitterSearch(
    consumer_key=os.environ.get('consumer_key', None),
    consumer_secret=os.environ.get('consumer_secret', None),
    access_token=os.environ.get('access_token', None),
    access_token_secret=os.environ.get('access_token_secret', None),
)


def tweetList(tso: TwitterSearchOrder) -> list:
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

    # Adding data to get better format of date time.
    timeNow = datetime.now().replace(tzinfo=timezone("Asia/Calcutta"))
    timeFormat = "%a %b %d %H:%M:%S %z %Y"

    # Loop to filter tweets
    for tweet in ts.search_tweets_iterable(tso):
        # Setting time difference field in tweet

        timetweet = datetime.strptime(tweet["created_at"], timeFormat)
        timetweet = timetweet.replace(tzinfo=timezone("Asia/Calcutta"))
        timeDiff = timeNow - timetweet

        minutes = timeDiff.seconds // 60
        hours = minutes // 60
        days = timeDiff.days

        if days:
            tweet['timeDiff'] = f"{days}d"
        elif hours:
            tweet['timeDiff'] = f"{hours}h"
        else:
            tweet['timeDiff'] = f"{minutes}m"

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
        print(f"{tweet['user']['screen_name']}:  {tweet['timeDiff']}")
        for line in tweet["full_text"].split("\n"):
            print(f"\t{line}")

    print(f"Tweet Fetched: {len(tweetsList)}")
    print('='*40)  # ending line
    print()  # empty line


def getResourceTSO(keywords: list, stopWords: list = None, resultType: str = 'recent', verified: bool = True) -> TwitterSearchOrder:
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

    # This remove retweets improve performance
    # around 5 times from 1200 tweets filtering
    # to just 200 to 300 now.
    keywords.append('-filter:retweets')

    if verified:
        keywords.append('verified')

    if stopWords == None:
        stopWords = [
            'need',
            'needs',
            'needed',
            'any',
            'require',
            'request',
            'required',
            'requires',
            'requirement',
            'golden'
        ]

    tso = TwitterSearchOrder()
    tso.set_keywords(keywords)

    for word in stopWords:
        tso.add_keyword(f'-"{word}"')

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

    ResouceTSO = getResourceTSO(keywords, stopWords)

    return tweetList(ResouceTSO)


class CovidResourceTSOs:

    def __init__(self,) -> None:

        city = 'jaipur'

        self.Remdesivir = getResourceTSO(["remdesivir", city])

        self.Tocilizumab = getResourceTSO(["Tocilizumab", city])

        self.Food = getResourceTSO(["food", city], stopWords=[])

        OxBedstopWords = [
            'need',
            'needs',
            'needed',
            'any',
            'required',
            'require',
            'requires',
            'requirement',
            'without',
            'golden'
        ]
        self.OxygenBeds = getResourceTSO(
            ["beds", "oxygen", city], stopWords=OxBedstopWords)

        self.OxygenCylinder = getResourceTSO(["Oxygen", "cylinder", city])

        self.HospitalBeds = getResourceTSO(["beds", city])

        self.ICUbeds = getResourceTSO(["icu", city])

        self.News = getResourceTSO(
            ["News", "covid", city], stopWords=[], verified=False)

        self.Plasma = getResourceTSO(["PLASMA", city])



if __name__ == "__main__":

    city = "jaipur"

    # REMDESIVIR FETCH
    remdesivirKeywords = ["remdesivir", city]
    # printTweets("REMDESIVIR", getResourceTweets(remdesivirKeywords))

    # FOOD FETCH
    foodKeywords = ["food", "covid", city]
    # printTweets("FOOD", getResourceTweets(foodKeywords, stopWords=[]))

    # OXYGEN BED FETCH
    oxygenBedKeywords = ["beds", "oxygen", city]
    # stopWords = [
    #     'need',
    #     'needs',
    #     'needed',
    #     'any',
    #     'required',
    #     'require',
    #     'requires',
    #     'requirement',
    #     'without',
    #     'golden'
    # ]
    # printTweets("OXYGEN BED", getResourceTweets(oxygenBedKeywords, stopWords))

    # OXYGEN CYLINDER FETCH
    oxygenCylinderKeywords = ["Oxygen", "cylinder", city]
    # printTweets("OXYGEN CYLINDER", getResourceTweets(oxygenCylinderKeywords))

    # HOSPITAL BED FETCH
    hospitalBedKeywords = ["beds", city]
    # printTweets("HOSPITAL BEDS", getResourceTweets(hospitalBedKeywords))

    # ICU FETCH
    ICUKeywords = ["icu", city]
    # printTweets("ICU", getResourceTweets(ICUKeywords))

    # NEWS FETCH
    NEWSKeywords = ["News", "covid", city]
    # printTweets("NEWS", getResourceTweets(NEWSKeywords))

    # TOCILIZUMAB FETCH
    TOCILIZUMABKeywords = ["Tocilizumab", city]
    # printTweets("TOCILIZUMAB", getResourceTweets(TOCILIZUMABKeywords))

    # VENTILATOR FETCH
    VENTILATORKeywords = ["VENTILATOR", city]
    # printTweets("VENTILATOR", getResourceTweets(VENTILATORKeywords))

    # PLASMA FETCH
    PLASMAKeywords = ["PLASMA", city]
    # printTweets("PLASMA", getResourceTweets(PLASMAKeywords))
