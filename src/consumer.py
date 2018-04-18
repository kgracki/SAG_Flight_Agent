'''
Created on 16 kwi 2018

@author: Kacper
'''
# model.py
from mesa import Agent, Model
from mesa.time import RandomActivation
import random


class EmailAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Email Agent"
        self.wealth = 999
        
    def print_agent_data(self):
        print("Agent id: ", self.unique_id)
        print("Agent name: ", self.name)
    
    def step(self):
        self.print_agent_data()
    
class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
    
    def print_agent_data(self):
        print("Agent id: ", self.unique_id)
        print("Agent wealth: ", self.wealth)
        
    def step(self):
        # The agent's step will go here.
        if self.wealth == 0:
            return
        other_agent = random.choice(self.model.schedule.agents)
        other_agent.wealth += 1
        self.wealth -= 1
        self.print_agent_data()
    

        
class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
        self.schedule.add(EmailAgent(1111, self))

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()