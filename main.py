from re import sub
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Twitter_V4 import tweetList, CovidResourceTSOs
from send_mail import send_volunteer_email, Volunteer
from get_db import (
    get_resources,
    connect_db,
    put_resources,
    Item,
    get_bed,
    put_subscriber,
    get_subscriber_single,
    Subscriber,
    put_volunteer,
    Volunteer,

    put_channel,
    get_channel,
    get_channel_by_district,
    Channel
)


# Object of class containing TSO for different resources.
ResourceTSO = CovidResourceTSOs()

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.get('/getConcentrator')
def getNews():
    return(returnDict(tweetList(ResourceTSO.Concentrator)))


'''
Endpoints for DB.
'''


@app.get('/getResource/{resource}')
def getResource(resource, start: int=0, end: int=10):
    db = connect_db()
    # print(resource)
    data = get_resources(db, resource, start, end)
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


@app.post('/putSubscriber/')
async def putSubscriber(subscriber: Subscriber):
    db = connect_db()
    check_user = get_subscriber_single(db, subscriber)
    if check_user:
        Channel_distric = get_channel_by_district(db, check_user["Distric_id"])

        if Channel_distric != None:
            chat_url = Channel_distric["Chat_url"]
            chat_name = Channel_distric["Name"]
            return {
                'Name': chat_name,
                'link': chat_url,
                'success': "Already exist"
            }
        else:
            return {
                'suceess' : 'Already exist',
                'link' : 'None' 
            }
    else:
        ins_id = put_subscriber(db, subscriber)
        if ins_id != '':
            Channel_distric = get_channel_by_district(db, subscriber.Distric_id)
            if Channel_distric != None:
                chat_url = Channel_distric["Chat_url"]
                chat_name = Channel_distric["Name"]
                return {
                    'Name': chat_name,
                    'link': chat_url,
                    'success': ins_id
                }
            else:
                return {
                    'suceess' : ins_id,
                    'link' : 'None' 
                }
            
        else:
            return {'fail'}



@app.get('/getSubscriber/')
def getSubscriber():
    return {
        "Kuch nah milna ": " ; )"
    }


@app.post('/putVolunteer/')
async def putResource(volunteer: Volunteer):
    db = connect_db()
    ins_id = put_volunteer(db, volunteer)
    if ins_id != '':
        ret = send_volunteer_email(volunteer)
        return {'success'}
    else:
        #ret = send_email(volunteer, 'Fails')
        return {'fail'}

@app.post('/putChannel/')
async def putChannel(channel: Channel):
    db = connect_db()
    ins_id = put_channel(db, channel)
    if ins_id != '':
        return {'success'}
    else:
        return {'fail'}

@app.get('/getChannel/')
def getChannel():
    db = connect_db()
    data = get_channel(db)
    return JSONResponse(content=data)

@app.get('/getChannelDistrictId/{distric_id}')
def getChannel(distric_id):
    db = connect_db()
    Channel_distric = get_channel_by_district(db, distric_id)
    if Channel_distric:
        chat_url = Channel_distric["Chat_url"]
        chat_name = Channel_distric["Name"]
        return {
            'Name': chat_name,
            'link': chat_url,
            'success': 'yep'
        }
    else:
        return{
            'success': 'nope'
        }

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    #port = int(process.env.PORT)
    #uvicorn.run("main:app", reload=True)
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
