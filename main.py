'''
Created on 16 kwi 2018

@author: Kacper Gracki
'''

from consumer import *
from flight_webscrap import check_flights_azair, check_promotion_fru
from email_notification import send_email
from pulsar.apps import http
from pulsar.apps.ds.parser import response_error
session = http.HttpClient

async def mycoroutine():
    response = await session.get("https://www.fru.pl/bilety-lotnicze/promocje")
    request = response.request()
    print(request.headers)
    
    return response.text()

# mycoroutine()


# empty_model = MoneyModel(10)
# for i in range(2):
#     empty_model.step()


check_promotion_fru()
check_flights_azair(3, 6)
# send_email("284")

print("end")