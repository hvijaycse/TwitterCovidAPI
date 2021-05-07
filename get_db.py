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


'''
DB Object Models
'''

class Item(BaseModel):
    #_id: Optional[str] = None
    Name: Optional[str] = None
    Area: Optional[str] = None
    Contact: Optional[str] = None
    Resource: Optional[str] = None
    Description: Optional[str] = None
    Price: Optional[str] = None
    City: Optional[str] = None
    Verified: Optional[str] = None
    Image: Optional[str] = None
    Time: Optional[str] = None

class Subscriber(BaseModel):
    Name: Optional[str] = None
    Email: Optional[str] = None
    Contact: Optional[str] = None
    Min_age: Optional[str] = None
    Distric_id: Optional[str] = None
    Pincode: Optional[str] = None


class Volunteer(BaseModel):
    #_id: Optional[str] = None
    Name: Optional[str] = None
    Email: Optional[str] = None
    Contact: Optional[str] = None
    Min_age: Optional[str] = None
    Distric_id: Optional[str] = None
    Pincode: Optional[str] = None


'''
Method to connect to DB
'''
def connect_db():
    dbUsername = os.environ.get('db_username', None)
    dbPass = os.environ.get('db_pass', None)
    client = pymongo.MongoClient(f"mongodb+srv://{dbUsername}:{dbPass}@cluster0.w3mep.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test_database
    return db

'''
Method to get and put resources in DB
'''

def get_resources(db, resource):
    search_string = {"Resource": resource}
    curso = db.covid_resources.find(search_string)
    ret = []
    for item in curso:
            data= {}
            if "Name"in item.keys():
                data["Name"] = item['Name']
            if "Area"in item.keys():
                data["Area"] = item['Area']
            if "Contact number"in item.keys():
                data["Contact number"] = item['Contact number']
            if "Resource"in item.keys():
                data["Resource"] = item['Resource']
            if "Description"in item.keys():
                data["Description"] = item['Description']
            if "Price"in item.keys():
                data["Price"] = item['Price']
            if "City"in item.keys():
                data["City"] = item['City']
            if "Verified"in item.keys():
                data["Verified"] = item['Verified']
            if "Image"in item.keys():
                data["Image"] = item['Image']
            if "Time"in item.keys():
                data["Time"] = item['Time']    
            ret.append(data)
             

    return ret 

def put_resources(db, item:Item):
    data  = {
            "Name": item.Name, 
            "Area":item.Area, 
            "Contact number": item.Contact, 
            "Resource": item.Resource, 
            "Description": item.Description,
            "Price": item.Price,
            "City": item.City,
            "Verified": item.Verified,
            "Image": item.Image,
            "Time": item.Time
            }
    ins_id = db.covid_resources.insert_one(data).inserted_id
    ret = ''
    if ins_id != '':
        ret = { "success" : ins_id}
    jsonString = dumps(ret)
    return jsonString

'''
Methods to get live BED status from DB.
'''

def get_bed(db, city):
    search_string = {"City": city}
    curso = db.bed_tracker.find(search_string)
    ret = []
    for item in curso:
            data= {}
            if "City"in item.keys():
                data["City"] = item['City']
            if "Hospital"in item.keys():
                data["Hospital"] = item['Hospital']
            if "Gen_Bed_T"in item.keys():
                data["Gen_Bed_T"] = item['Gen_Bed_T']
            if "Gen_Bed_O"in item.keys():
                data["Gen_Bed_O"] = item['Gen_Bed_O']
            if "Gen_Bed_A"in item.keys():
                data["Gen_Bed_A"] = item['Gen_Bed_A']
            if "Oxy_Bed_T"in item.keys():
                data["Oxy_Bed_T"] = item['Oxy_Bed_T']
            if "Oxy_Bed_O"in item.keys():
                data["Oxy_Bed_O"] = item['Oxy_Bed_O']
            if "Oxy_Bed_A"in item.keys():
                data["Oxy_Bed_A"] = item['Oxy_Bed_A']
            if "ICU_Bed_wov_T"in item.keys():
                data["ICU_Bed_wov_T"] = item['ICU_Bed_wov_T']
            if "ICU_Bed_wov_O"in item.keys():
                data["ICU_Bed_wov_O"] = item['ICU_Bed_wov_O']
            if "ICU_Bed_wov_A"in item.keys():
                data["ICU_Bed_wov_A"] = item['ICU_Bed_wov_A']   
            if "ICU_Bed_wv_T"in item.keys():
                data["ICU_Bed_wv_T"] = item['ICU_Bed_wv_T']   
            if "ICU_Bed_wv_O"in item.keys():
                data["ICU_Bed_wv_O"] = item['ICU_Bed_wv_O']   
            if "ICU_Bed_wv_A"in item.keys():
                data["ICU_Bed_wv_A"] = item['ICU_Bed_wv_A']
            if "Contact_Number"in item.keys():
                data["Contact_Number"] = item['Contact_Number']
            ret.append(data)
    return ret 

'''
Method to get and put subscriber
'''

def put_subscriber(db, subscriber:Subscriber):
    data  = {
            "Name": subscriber.Name, 
            "Email":subscriber.Email, 
            "Contact_number": subscriber.Contact, 
            "Minmum_age": subscriber.Min_age, 
            "Distric_id": subscriber.Distric_id,
            "Pincode": subscriber.Pincode
            }
    ins_id = db.subscriber.insert_one(data).inserted_id
    ret = ''
    if ins_id != '':
        ret = { "success" : ins_id}
    jsonString = dumps(ret)
    return jsonString



def get_subscriber(db):
    curso = db.subscriber.find({})
    ret = []
    for item in curso:
            data= {}
            if "Name"in item.keys():
                data["Name"] = item['Name']
            if "Email"in item.keys():
                data["Email"] = item['Email']
            if "Contact_number"in item.keys():
                data["Contact_number"] = item['Contact_number']
            if "Minmum_age"in item.keys():
                data["Minmum_age"] = item['Minmum_age']
            if "Distric_id"in item.keys():
                data["Distric_id"] = item['Distric_id']
            if "Pincode"in item.keys():
                data["Pincode"] = item['Pincode']   
            ret.append(data)
    return ret 


def get_subscriber_single(db, subscriber:Subscriber):
    find_string = {
            "Email":subscriber.Email,
            "Contact_number": subscriber.Contact
            }
    cursor = db.subscriber.find(find_string)
    count = 0
    for item in cursor:
        count +=1
    
    if count == 0:
        print('')
    else:
        print("X")

'''
Method to put and get Volunteer
'''

def put_volunteer(db, volunteer:Volunteer):
    data  = {
            "Name": volunteer.Name, 
            "Email":volunteer.Email, 
            "Contact_number": volunteer.Contact, 
            "Minmum_age": volunteer.Min_age, 
            "Distric_id": volunteer.Distric_id,
            "Pincode": volunteer.Pincode
            }
    ins_id = db.volunteer.insert_one(data).inserted_id
    ret = ''
    if ins_id != '':
        ret = { "success" : ins_id}
    jsonString = dumps(ret)
    return jsonString



def get_volunteer(db):
    curso = db.volunteer.find({})
    ret = []
    for item in curso:
            data= {}
            if "Name"in item.keys():
                data["Name"] = item['Name']
            if "Email"in item.keys():
                data["Email"] = item['Email']
            if "Contact_number"in item.keys():
                data["Contact_number"] = item['Contact_number']
            if "Minmum_age"in item.keys():
                data["Minmum_age"] = item['Minmum_age']
            if "Distric_id"in item.keys():
                data["Distric_id"] = item['Distric_id']
            if "Pincode"in item.keys():
                data["Pincode"] = item['Pincode']   
            ret.append(data)
    return ret 
