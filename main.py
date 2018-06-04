'''
Created on 16 kwi 2018

@author: Kacper Gracki
'''

from consumer import *
from flight_webscrap import check_flights_azair, check_promotion_fru
from email_notification import send_email
from pulsar.apps import http
from pulsar.apps.ds.parser import response_error
from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send, Event, get_actor
from openpyxl.styles.builtins import comma
import asyncio


# session = http.HttpClient

# async def mycoroutine():
#     response = await session.get("https://www.fru.pl/bilety-lotnicze/promocje")
#     request = response.request()
#     print(request.headers)
#     
#     return response.text()
# 
# check_promotion_fru()
# check_flights_azair(3, 6)
# send_email("284")



names = ['john', 'luca', 'carl', 'jo', 'alex']

@command()
def greetme(request, message):
    echo = 'Hello {}!'.format(message['name'])
    request.actor.logger.info(echo)
    
    return echo

@command()
def email_callback(request, message):
    echo = "It's email agent!"
    request.actor.logger.info(echo)
    send_email(message)
    
    return echo

@command()
async def check_flights(request, message):
    echo = "Agent {}".format(message)
    request.actor.logger.info(echo)
    price = await check_flights_azair(2, 6)
    print(price)
    
    return echo

def say_hello(arg,  **kw):
    print("Agent called {} started working".format(arg, kw))

def periodic_ping(arg,  **kw):
    print("Agent called {} is alive".format(arg, kw))


class FlightCheck:
    
    def __init__(self):
        arb = arbiter()
        self._loop = arb._loop
        self._loop.call_later(1, self)

        arb.start()
    
    def __call__(self, a=None, b=None):
        ensure_future(self._work(a, b))
    

    async def _work(self, a=None, b=None):
        if a is None:
            a = await spawn(name='greeter', start=say_hello, periodic_task=periodic_ping)
        if b is None:
            b = await spawn(name='flight_agent', start=say_hello, periodic_task=periodic_ping)
        
#         c = await spawn(name="email_agent")
            
#         if email is None:
#             email = await spawn(name='email_agent')
#         if e is None:
#             e = Event(name="test_event", o="bleble", onetime=True)
#             e.bind(say_hello)
        if names:
            name = names.pop()
#             self._loop.logger.info("Creating: {}".format(name))
            await send(a, 'greetme', {'name': name})
           
#             self._loop.call_soon(ensure_future, self(a, b))
            self._loop.call_later(1, self, a, b)
            
        else:
            await send(a, 'stop')
            await send(b, 'check_flights', {'name': "FRU"})
            self._loop.call_later(100, self, a, b)
#             arbiter().stop()
    

if __name__ == '__main__':
    FlightCheck()