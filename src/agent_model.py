from asyncio import ensure_future
from pulsar.api import arbiter, command, spawn, send, Event, get_actor
from PyPDF2.pdf import __maintainer_email
from asyncio.tasks import wait
from test.test_iterlen import NoneLengthHint
from numpy import equal
from turtle import done


names = ['john', 'luca', 'carl', 'jo', 'alex']

@command()
def greetme(request, message):
    echo = 'Hello {}!'.format(message['name'])
    request.actor.logger.info(echo)
    
    return echo

@command()
def email_callback(request, message):
    echo = "It's email agent {}!".format(message['name'])
    request.actor.logger.info(echo)
    
    return echo

def say_hello(arg,  **kw):
    print("Yooo ", arg, kw)


class Greeter:
    
    def __init__(self):
        arb = arbiter()
        self._loop = arb._loop
        self._loop.call_later(1, self)

        arb.start()

    def __call__(self, a=None, b=None):
        ensure_future(self._work(a, b))
    

    async def _work(self, a=None, b=None):
        if a is None:
            a = await spawn(name='greeter')
        if b is None:
            b = await spawn(name='email_agent')
#         if email is None:
#             email = await spawn(name='email_agent')
#         if e is None:
#             e = Event(name="test_event", o="bleble", onetime=True)
#             e.bind(say_hello)
        if names:
            name = names.pop()

            await send(a, 'greetme', {'name': name})
            await send(b, 'email_callback', {'name': "Kacper"})
            
            self._loop.call_later(1, self, a , b)
            
        else:
            arbiter().stop()
    

if __name__ == '__main__':
    Greeter()
    