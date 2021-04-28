# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:25:18 2021

@author: gauravvijayvergiya
"""

import pymongo
from json import dumps
from pydantic import BaseModel
from typing import Optional
import os

#client = pymongo.MongoClient(f'mongodb+srv://cluster0.w3mep.mongodb.net/myFirstDatabase" --username {username} --passowrd {passs}')


class Item(BaseModel):
    #_id: Optional[str] = None
    Name: Optional[str] = None
    Area: Optional[str] = None
    Contact: Optional[str] = None
    Resource: Optional[str] = None
    Description: Optional[str] = None
    Price: Optional[str] = None
    City: Optional[str] = None
    Verifed: Optional[str] = None
    Image: Optional[str] = None

def connect_db():
    dbUsername = os.environ.get('db_username', None)
    dbPass = os.environ.get('db_pass', None)
    client = pymongo.MongoClient(f"mongodb+srv://{dbUsername}:{dbPass}@cluster0.w3mep.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test_database
    return db

def get_resources(db, resource):
    search_string = {"Resourse": resource}
    #print(search_string)
    list_cur = list(db.covid_resources.find(search_string))
    # Converting to the JSON
    json_data = dumps(list_cur, indent = 2)
    #print(json_data)
    return json_data 

def put_resources(db, item:Item):
    #search_string = '{"Resourse": "'+resource+'"}'
    data  = {
            "Name": item.Name, 
            "Area":item.Area, 
            "Contact number": item.Contact, 
            "Resourse": item.Resource, 
            "Description": item.Description,
            "Price": item.Price,
            "City": item.City,
            "Verifed": item.Verifed,
            "Image": item.Image,
            }
    ins_id = db.covid_resources.insert_one(data).inserted_id
    #list_cur = list(db.covid_resources.find(search_string))
    #jsonString = dumps(list_cur)
    #print(data)
    return ins_id