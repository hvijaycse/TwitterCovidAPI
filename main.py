from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Twitter_V4 import getResourceTweets
from get_db import get_resources, connect_db, put_resources,Item

app = FastAPI()

city = 'jaipur'
origins = ['*']

app.add_middleware(CORSMiddleware,  allow_origins=origins,
                   allow_credentials=False,  allow_methods=["*"],  allow_headers=["*"], )


def returnDict(tweets: list) -> dict:

    newDict = {
        "tweetCount": len(tweets)
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
    remdesivirKeywords = ["remdesivir", "verified", city]
    return(returnDict(getResourceTweets(remdesivirKeywords)))


@app.get('/getToc')
def getTocilizumab():
    TOCILIZUMABKeywords = ["Tocilizumab", "verified", city]
    return(returnDict(getResourceTweets(TOCILIZUMABKeywords)))


@app.get('/getFood')
def getFood():
    foodKeywords = ["food", "covid", city]
    return(returnDict(getResourceTweets(foodKeywords, stopWords=[])))


@app.get('/getOxygenCylinder')
def getOxygenCylinder():
    oxygenCylinderKeywords = ["Oxygen", "cylinder", "verified", city]
    return(returnDict(getResourceTweets(oxygenCylinderKeywords)))


@app.get('/getOxygenBed')
def getOxygenBed():
    oxygenBedKeywords = ["oxygen", "bed", "verified", city]
    return(returnDict(getResourceTweets(oxygenBedKeywords)))


@app.get('/getHb')
def gethospitalBed():
    hospitalBedKeywords = ["bed", "verified", city]
    return(returnDict(getResourceTweets(hospitalBedKeywords)))


@app.get('/getICU')
def getICU():
    ICUKeywords = ["ICU", "verified", city]
    return(returnDict(getResourceTweets(ICUKeywords)))


@app.get('/getNews')
def getNews():
    newsKeywords = ["News", "covid", city]
    return(returnDict(getResourceTweets(newsKeywords)))


@app.get('/getResource/{resource}')
def getResource(resource):
    db = connect_db()
    # print(resource)
    data = get_resources(db, resource)
    # print(data)
    return JSONResponse(content=data)


@app.post('/putResource/')
async def putResource(item: Item):
    db = connect_db()
    ins_id = put_resources(db,item)
    if ins_id != '':
        return {'success' : ins_id}
    else:
        return {'fail'}
    
