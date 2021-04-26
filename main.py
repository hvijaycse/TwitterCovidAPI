from Twitter_V4 import getResourceTweets
from fastapi import FastAPI


app = FastAPI()
city = 'jaipur'


def returnDict(tweets: list) -> dict:

    newDict= {
        "tweetCount" : len(tweets)
    } 

    for i, tweet in enumerate(tweets):
        newDict[i] = tweet

    return newDict

@app.get("/")
def home():

    return {
        "GET WELL": "JAIPUR"
    }


@app.get('/getRem')
def getRemdesivir():
    remdesivirKeywords = ["remdesivir", "available", "verified", city]
    return(returnDict(getResourceTweets(remdesivirKeywords)))


@app.get('/getfood')
def getFood():
    foodKeywords = ["Food", "covid", city]
    return(returnDict(getResourceTweets(foodKeywords)))


@app.get('/getOxygen')
def getOxygen():
    oxygenKeywords = ["Oxygen", "available", "verified", city]
    return(returnDict(getResourceTweets(oxygenKeywords)))


@app.get('/getHb')
def gethospitalBed():
    hospitalBedKeywords = ["bed", "available",  "covid", city]
    return(returnDict(getResourceTweets(hospitalBedKeywords)))


@app.get('/getICU')
def getICU():
    icuKeywords = ["ICU", "available", city]
    return(returnDict(getResourceTweets(icuKeywords)))


@app.get('/getNews')
def getNews():
    newsKeywords = ["News", "covid", city]
    return(returnDict(getResourceTweets(newsKeywords)))
