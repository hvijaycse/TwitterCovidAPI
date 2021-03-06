# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 17:59:05 2021

@author: gauravvijayvergiya
"""
"""
'City'	:	'City'
'Hospital'	:	'Hospital'
'Gen_Bed_T'	:	'General Bed Total'
 'Gen_Bed_O'	:	'General Bed Occupid'
 'Gen_Bed_A'	:	'General Bed Available'
 'Oxy_Bed_T'	:	'Oxygen Bed Total'
 'Oxy_Bed_O'	:	'Oxygen Bed Occupide'
 'Oxy_Bed_A'	:	'Oxygen Bed Available'
 'ICU_Bed_wov_T'	:	'ICU bed without ventilator Total'
 'ICU_Bed_wov_O'	:	'ICU bed without ventilator Occupide'
'ICU_Bed_wov_A'	:	'ICU bed without ventilator Available' 
 'ICU_Bed_wv_T'	:	'ICU bed with ventilator Total'
 'ICU_Bed_wv_O'	:	'ICU bed with ventilator Occupide'
 'ICU_Bed_wv_A'	:	'ICU bed with ventilator Available'


"""




import requests
from urllib.request import urlopen
import pymongo
import os
from bs4 import BeautifulSoup
def updateBed_job():
    '''
    This method is used to update the live bed data 
    in database. 
    This is executed every hour using heroku clock.
    '''

    print("Cron job is running")
    dbUsername = os.environ.get('db_username', None)
    dbPass = os.environ.get('db_pass', None)
    url = 'https://covidinfo.rajasthan.gov.in/Covid-19hospital-wisebedposition-wholeRajasthan.aspx'

    try:

        print("Trying to fetch data.")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        client = pymongo.MongoClient(
            f"mongodb+srv://{dbUsername}:{dbPass}@cluster0.w3mep.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        count = 0
        all_data = []
        for tr in soup.find_all("tr"):

            td = tr.find_all("td")
            # print(td)
            if len(td) >= 16:
                count += 1
                data = {
                    'City': td[1].text,
                    'Hospital': td[2].text,
                    'Gen_Bed_T': td[3].text,
                    'Gen_Bed_O': td[4].text,
                    'Gen_Bed_A': td[5].text,
                    'Oxy_Bed_T': td[6].text,
                    'Oxy_Bed_O': td[7].text,
                    'Oxy_Bed_A': td[8].text,
                    'ICU_Bed_wov_T': td[9].text,
                    'ICU_Bed_wov_O': td[10].text,
                    'ICU_Bed_wov_A': td[11].text,
                    'ICU_Bed_wv_T': td[12].text,
                    'ICU_Bed_wv_O': td[13].text,
                    'ICU_Bed_wv_A': td[14].text,
                    'Contact_Number': td[15].text,
                    # 'Contact_Hospital': td[16].text,
                }
                all_data.append(data)

        # print(all_data)
        if count == 0:
            print("Website may be down")
        else:
            print("Website is up")
            db = client.test_database
            db.bed_tracker.delete_many({})
            ins_id = db.bed_tracker.insert_many(all_data)

            print('Record inserted', ins_id.acknowledged)

            cur = db.bed_tracker.find()
            insert_count = 0
            for item in cur:
                insert_count += 1
            print('Record inserted:', count, 'Record in DB:', insert_count)
    except:
        print("An error has occur.")

    # Calling heroku api so that
    # free dyno doesn't go down


def callServer():

    print("Calling service")
    herokurl = "https://cjaipur.herokuapp.com/"
    urlopen(herokurl)


if __name__ == "__main__":
    updateBed_job()

"""


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
            "Time": item.Time
            }
    ins_id = db.covid_resources.insert_one(data).inserted_id

<td style="text-align: center">404</td>,
city  <td>Udaipur</td>,
hostpital  <td><b>Sunrise Hospital</b></td>,
 GBT <td>0</td>, 
 GBO <td>0</td>,
 GBA <td style="color:red;font-size:18px;">0</td>,
 OBT <td>13</td>,
 OBO <td>13</td>, 
 OBA  <td style="color:red;font-size:18px;">0</td>, 
 ICUT <td>6</td>, 
 ICUO <td>6</td>, 
 ICUA <td style="color:red;font-size:18px;">0</td>, 
 ICUWVT <td>2</td>, 
 ICUWVO <td>2</td>, 
 ICUWVA <td style="color:red;font-size:18px;">0</td>, 
 Hospital helpline number<td>8107288889</td>, 
dist.contorl number  <td>6367304312</td>]
    
    """
