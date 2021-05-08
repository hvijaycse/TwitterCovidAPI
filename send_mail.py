# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:44:53 2021

@author: gauravvijayvergiya
"""
import smtplib
import ssl
from get_db import Volunteer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

smtp_server = os.environ.get("smtp_server", None)
port = 587  # For starttls
sender_email = os.environ.get("smtp_mail", None)
password = os.environ.get("smtp_pass", None)


receiver_email = ["amanvijay.cs@gmail.com",
                  "hvijay.cse@gmail.com", "gauravvijayvergiya@gmail.com"]



def send_volunteer_email(volunteer: Volunteer):
    receiver_email = [
        "amanvijay.cs@gmail.com",
        "hvijay.cse@gmail.com",
        "gauravvijayvergiya@gmail.com"
    ]

    subject = 'New Volunteer for covid19 assist.'

    body = """
    voila!!
    A new Volunteer for your cool Idea

    My detials are:
        Name: {}
        Email: {}
        Contact: {}
        City: {}
        Pincode: {}
        Add To Group: {}
        
    Thanks,
    Covid Assist bot
    """.format(
        volunteer.Name,
        volunteer.Email,
        volunteer.Contact,
        volunteer.City,
        volunteer.Pincode,
        volunteer.Add_to_group
    )
    send_email(
        receiver_email=receiver_email,
        subject=subject, 
        body=body
    )

def prepare_email(volunteer: Volunteer):
    
    subject = 'New Volunteer for covid19 assist.'

    body = """
    voila!!
    A new Volunteer for your cool Idea

    My detials are:
        First Name: {}
        Last Name: {}
        Contact: {}
        Email: {}
        City: {}
        Zipcode: {}
        Addtochat: {}
        
    Thanks,
    Covid Assist bot
    """.format(
        volunteer.FirstName,
        volunteer.LastName,
        volunteer.Contact,
        volunteer.Email,
        volunteer.City,
        volunteer.Zipcode,
        volunteer.Addtochat
    )
    send_email(sender_email=sender_email, receiver_email=[],
               subject=subject, body=body)
    #    body = 'YOUR TEXT'


def send_email(receiver_email=receiver_email, subject='', body='No body'):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Bcc'] = ", ".join(receiver_email)
    msg['Subject'] = subject
    msg['X-MSMail-Priority'] = '1'
    msg.attach(MIMEText(body, 'plain'))
    message = msg.as_string()
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        return False
    finally:
        server.quit()
    print('mail sent')
    return True
