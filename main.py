'''
Created on 16 kwi 2018

@author: Kacper Gracki
'''

from consumer import *
from flight_webscrap import check_flights, check_promotion_fru
from email_notification import send_email


empty_model = MoneyModel(10)
for i in range(2):
    empty_model.step()

check_promotion_fru()
# check_flights(3, 6)
# send_email("284")

print("end")