"""Simple actor message passing"""
from pulsar.api import arbiter, spawn, send, ensure_future, Config, get_actor

from consumer import *
from flight_webscrap import check_flights_azair, check_promotion_fru
from email_notification import send_email
from pulsar.apps import http
from pulsar.apps.ds.parser import response_error
from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send, Event, get_actor
from openpyxl.styles.builtins import comma
import asyncio
from turtledemo.penrose import star
from _collections_abc import coroutine
from email import message



    
def say_hello(arg,  **kw):
    print("Actor called {} started working".format(arg, kw))

def periodic_ping(arg,  **kw):
    print("Actor called {} is alive".format(arg, kw))
    actor = get_actor()
    print(actor.name)
    
    
# @command()
async def check_flights(actor, message):
    print("Actor {} message: {}".format(actor.name, message))
    price = await check_flights_azair(2, 6)
    
    return price

def check_promotion(actor, message):
    print("Actor {} message: {}".format(actor.name, message))
    check_promotion_fru()
    

def bleble(actor, message):
    print("Actor {} message: {}".format(actor.name, message))
    

async def test():
    print("TEST EVENT")
    actor_test = await spawn(name='test', star=say_hello, periodic_task=periodic_ping)
    await send(actor_test, 'run', inner_method, 1)
    value = await send(actor_test, 'run', get_value)
    print(value)
    value = value + 1
    await send(actor_test, 'run', set_value, value)
    value = await send(actor_test, 'run', get_value)
    print(value)
    
    arb = get_actor()
    print(arb)
    await send(arb, 'run', bleble, "AFTER TEST")
    arb._loop.call_later(2, start, actor_test)
    

        
def start(arb, actor_azair=None, actor_fru=None):    
    ensure_future(app(actor_azair, actor_fru))
#     ensure_future(test())
    
iteration_azair = 0
iteration_fru = 0

async def app(actor_azair=None, actor_fru=None):
    global iteration_azair, iteration_fru
    # Spawn a new actor
    if actor_azair is None:
        actor_azair = await spawn(name='actor_azair', start=say_hello, periodic_task=periodic_ping)
        iteration_azair = 0
        await send(actor_azair, 'run', inner_method, iteration_azair)
    if actor_fru is None:
        actor_fru = await spawn(name='actor_fru', start=say_hello, periodic_task=periodic_ping)
        iteration_fru = 0
        await send(actor_fru, 'run', inner_method, iteration_fru)
        
    # Execute inner method in actor1
#     result = await send(actor_fru, 'run', inner_method)
#     print(result)
    await send(actor_azair, 'run', set_value, iteration_azair)
    iteration_azair += 1
    value_azair = await send(actor_azair, 'run', get_value)
    print(value_azair)
    
    await send(actor_fru, 'run', set_value, iteration_fru)
    iteration_fru += 1
    value_fru = await send(actor_fru, 'run', get_value)
    print(value_fru)
    
    value = await send(actor_azair, 'run', check_flights, "AZAIR")
    print(value)
    
    await send(actor_fru, 'stop')
    await asyncio.sleep(10)
    
    arb = get_actor()
    print(arb.info())
#     print(arb)
    return (await app())
#     arb._loop.call_later(5, start, arb, actor_azair, actor_fru)

    # Stop the application
#     arbiter().stop()


async def stop(actor):
    print("Actor stop: ", actor.name)
    await send(actor, 'stop')
    
def inner_method(actor, value):
    print("It's actor: ", actor.name)
    actor.saved_value = value

def set_value(actor, value):
    print("It's actor: ", actor.name)
    actor.saved_value = value

def get_value(actor):
    print("It's actor: ", actor.name)
    return actor.saved_value


if __name__ == '__main__':
    cfg = Config()
    cfg.parse_command_line()
    arbiter(cfg=cfg, start=start).start()
