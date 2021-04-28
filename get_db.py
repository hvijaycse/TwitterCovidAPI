# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:25:18 2021

@author: gauravvijayvergiya
"""

import pymongo
from bson.json_util import dumps, loads
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
    Time: Optional[str] = None

def connect_db():
    dbUsername = os.environ.get('db_username', None)
    dbPass = os.environ.get('db_pass', None)
    client = pymongo.MongoClient(f"mongodb+srv://{dbUsername}:{dbPass}@cluster0.w3mep.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test_database
    return db

def get_resources(db, resource):
    search_string = {"Resourse": resource}
    curso = db.covid_resources.find(search_string)
    ret = []
    for item in curso:
            data  = {
            "Name": item['Name'], 
            "Area":item["Area"],
            "Contact number": item["Contact number"],
            "Resourse": item["Resourse"], 
            "Description": item["Description"], 
            "Price": item["Price"], 
            "City": item["City"], 
            "Verifed": item["Verifed"],
            "Image": item["Image"],
            "Time": item["Time"]
            }
            ret.append(data)
             

    return ret 

def put_resources(db, item:Item):
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
    if ins_id != '':
        ret = { "success" : ins_id}
    jsonString = dumps(ret)
    return jsonString