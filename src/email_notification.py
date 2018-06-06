'''
Created on 16 kwi 2018

@author: Kacper Gracki
'''
#!/usr/bin/python


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from constants import *
# from email.mime.message import MIMEMessage


async def send_email(best_price):
    msg = MIMEMultipart()
    message = "Hello, best price is: %s" % best_price
    msg['Subject'] = "Checking flights"
    to = MY_EMAIL
    gmail_user = BOT_EMAIL
    gmail_password = BOT_PASSWORD
    msg['From'] = gmail_user
    msg['To'] = to
#     msg['Message'] = 
    msg.attach(MIMEText(message))

    try:
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.sendmail(gmail_user, to, msg.as_string())
        s.close()
        print ("Successfully sent message")
        
        return True
    except:
        print ("Error: can not send message")
        
        return False
