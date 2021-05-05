from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Twitter_V4 import getResourceTSO, tweetList
from get_db import get_resources, connect_db, put_resources, Item, get_bed


class CovidResourceTSOs:

    def __init__(self) -> None:

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
        self.OxygenBeds = getResourceTSO(["beds", "oxygen", city], stopWords=OxBedstopWords)

        self.OxygenCylinder = getResourceTSO(["Oxygen", "cylinder", city])

        self.HospitalBeds = getResourceTSO(["beds", city])

        self.ICUbeds = getResourceTSO(["icu", city])

        self.News = getResourceTSO(["News", "covid", city], stopWords=[], verified=False)

        self.Plasma = getResourceTSO(["PLASMA", city])


ResourceTSO = CovidResourceTSOs()

app = FastAPI()

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


'''
Endpoint url
'''


@app.get("/")
def home():

    return {
        "GET WELL": "JAIPUR"
    }


'''
Endpoints for Twitter API.
'''


@app.get('/getRem')
def getRemdesivir():
    return(returnDict(tweetList(ResourceTSO.Remdesivir)))


@app.get('/getToc')
def getTocilizumab():
    return(returnDict(tweetList(ResourceTSO.Tocilizumab)))


@app.get('/getFood')
def getFood():
    return(returnDict(tweetList(ResourceTSO.Food)))


@app.get('/getOxygenCylinder')
def getOxygenCylinder():
    return(returnDict(tweetList(ResourceTSO.OxygenCylinder)))


@app.get('/getOxygenBed')
def getOxygenBed():
    return(returnDict(tweetList(ResourceTSO.OxygenBeds)))


@app.get('/getHb')
def gethospitalBed():
    return(returnDict(tweetList(ResourceTSO.HospitalBeds)))


@app.get('/getICU')
def getICU():
    return(returnDict(tweetList(ResourceTSO.ICUbeds)))


@app.get('/getNews')
def getNews():
    return(returnDict(tweetList(ResourceTSO.News)))

@app.get('/getPlasma')
def getNews():
    return(returnDict(tweetList(ResourceTSO.Plasma)))


'''
Endpoints for DB.
'''


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
    ins_id = put_resources(db, item)
    if ins_id != '':
        return {'success': ins_id}
    else:
        return {'fail'}


@app.get('/getBed/{city}')
def getResource(city):
    db = connect_db()
    data = get_bed(db, city)
    return JSONResponse(content=data)
