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
from pulsar.async.actor import Actor
from openpyxl.styles.builtins import comma
import asyncio


names = ['AGENT_AZAIR', 'AGENT_FRU', 'TEST_AGENT']

@command()
def greetme(request, message):
    echo = 'Hello {}!'.format(message['name'])
    request.actor.logger.info(echo)
    
    return echo

# @command()
async def email_callback(actor, message):
    print("Agent {} is sending message: {}".format(actor.name, message))
    
    return (await send_email(message))
    
    
# @command()
async def check_flights(actor, count):
    print("Actor {} is checking flights".format(actor.name))
    await send(actor, 'run', set_value, count)
    price = await check_flights_azair(2, 6)
    
    return price

# @command()
async def check_promotion(actor, count):
    print("Actor {} is checking promotion".format(actor.name))
    await send(actor, 'run', set_value, count)
#     echo = "Agent {}".format(message)
#     request.actor.logger.info(echo)
    price = await check_promotion_fru()
    print(price)
    
    return price

def say_hello(arg,  **kw):
    print("Agent {} started working".format(arg, kw))

def periodic_ping(arg,  **kw):
    print("Agent {} is alive".format(arg, kw))

async def checking_done(actor, price1, price2):
    print("Agent {} is checking prices...".format(actor.name))
    
#     best_flight = "TAJLANDIAAAAA"
    best_flight = price1
    email_actor = await spawn(name="email_actor", start=say_hello, periodic_task=periodic_ping)
    resp = await send(email_actor, 'run', email_callback, best_flight)
    if not resp:
        print("Trying one more time...")
        resp = await send(email_actor, 'run', email_callback, best_flight)
        if not resp:
            print("Sending was unsuccessful")
            await send(email_actor, 'stop')
    else:
        print("Sending was successful")    
        await send(email_actor, 'stop') 
    
    print("Agent {} checking prices done".format(actor.name))
    

def inner_method(actor, value):
    actor.saved_value = value

def set_value(actor, value):
    print("Setting value {} for actor {}: ".format(value, actor.name))
    actor.saved_value = value

def get_value(actor):
    print("It's actor: ", actor.name)
    return actor.saved_value


iteration_azair = 0
iteration_fru = 0

class FlightCheck:
    
    def __init__(self):
        arb = arbiter()
        self._loop = arb._loop
        self._loop.call_later(1, self)

        arb.start()
    
    def __call__(self, a=None, b=None, c=None):
        ensure_future(self._work(a, b, c))
    

    async def _work(self, a=None, b=None, c=None):
        global iteration_azair, iteration_fru
        
        if a is None:
            a = await spawn(name='greeter', start=say_hello, periodic_task=periodic_ping)
        if b is None or not b.is_alive():
            b = await spawn(name='flight_azair', start=say_hello, periodic_task=periodic_ping)
            iteration_azair = 0
            await send(b, 'run', inner_method, iteration_azair)
        if c is None or not c.is_alive():
            c = await spawn(name="flight_fru", start=say_hello, periodic_task=periodic_ping)
            iteration_fru = 0
            await send(c, 'run', inner_method, iteration_fru)

        if names:
            name = names.pop()
            await send(a, 'greetme', {'name': name})
            self._loop.call_later(1, self, a, b, c)
        else:
            await send(a, 'stop')
            best_price_azair = await send(b, 'run', check_flights, iteration_azair)
            iteration_azair += 1
            best_price_fru = await send(c, 'run', check_promotion, iteration_fru)
            iteration_fru += 1
            if b.is_alive():
                await send(b, 'stop')
            
            await send('arbiter', 'run', checking_done, best_price_azair, best_price_fru)
            
            self._loop.call_later(80, self, a, b, c)
#             arbiter().stop()
    

if __name__ == '__main__':
    FlightCheck()