import bisect
import time
import random

from stage import Stage
from customer import Customer
from agent import Agent
from event import Event

# This central data structure here is an event queue where processing each event can create future events.
# We process the first event and insert any new events generated at the right place in queue.
# Once the queue is empty, we're done!
# This way, we can fast-forward to future where an interesting event happens.
# This ensures that simulation finishes quickly.
# Interesting events for us are when either a customer or an agent becomes available.
# Hence, two event types: "arrived" and "serviced".

# This is a discrete simulation and so, we will model time in integer seconds
# We want to support arbitrary probability distributions for arrival_rate and servicing_rate
# Hence, we will use lambdas to model both of these.
class Office(object):
    
    def __init__(self, stages, arrival_rate, customer_selection_strategy, agent_selection_strategy, enable_gui=True, debug=False):
        self.stages = stages
        self.current_time = 0
        self.customers = []
        self.events_queue = []
        self.agents = []
        self.arrival_rate = arrival_rate
        self.customer_selection_strategy = customer_selection_strategy
        self.agent_selection_strategy = agent_selection_strategy
        self.debug = debug

        # new customers arrive in this state (all 3 stages are pending)
        initial_status = {k: "pending" for k, v in stages.items()}
        num_customers = self.arrival_rate(0) # invoking the lambda at t=0
        for i in range(num_customers):
            xpos = 250 + 60*(i % 12)
            ypos = 250 + 50*(i / 12)
            customer = Customer("c{}".format(i), dict(initial_status), xpos, ypos)

            # assuming getting a token takes 1 second
            customer.token_time = i
            customer.waiting_since = i
            
            self.customers.append(customer)
            event = Event(type="arrived",agent=None,customer=customer,time=i)
            bisect.insort(self.events_queue, event) # insert in sorting order

        # For each stage, create agents
        for i, s in enumerate(stages.keys()):
            for j in range(stages[s].num_agents):
                agent = Agent(stage=stages[s], id="{}{}".format(s,j), x=300, y=300)
                self.agents.append(agent)
        
        # Arrange all agents in a circle around the waiting area
        # Need to iterate over *all* agents and not stage-wise
        if enable_gui:
            for i, a in enumerate(self.agents):
                a.position_x = 600+560*cos(i*TAU/len(self.agents))
                a.position_y = 600+560*sin(i*TAU/len(self.agents))

    # Which customers are waiting for the given stage?            
    def find_available_customers(self, stage_name):
        return [c for c in self.customers if c.agent == None and c.status[stage_name] == "pending"]
    
    # Which agents are free for the given stages?            
    def find_available_agents(self, stage_names):
        return [a for a in self.agents if a.stage.name in stage_names and a.customer == None]
    
    # Assign a customer to an agent        
    def assign(self, customer, agent):
        customer.status[agent.stage.name] = "ongoing"
        customer.agent = agent
        agent.customer = customer
        agent.available_at = self.current_time + agent.stage.servicing_time()
        if self.debug:
            print("assigning {} to {} till {}".format(customer.id, agent.id, agent.available_at))
        new_event = Event(type="serviced",agent=agent,customer=customer,time=agent.available_at)
        bisect.insort(self.events_queue, new_event) # insert in the right order
        
    # Process servicing completed event
    def release(self, ev):
        if self.debug:
            print("releasing {} from {}".format(ev.customer.id, ev.agent.id))
        ev.agent.customer = None
        ev.customer.status[ev.agent.stage.name] = "done"
        ev.customer.agent = None
        ev.customer.waiting_since = self.current_time
        if ev.customer.is_finished(self.stages.keys()):
            if self.debug:
                print("customer {} is finished".format(ev.customer.id))
        else:
            agents = self.find_available_agents(ev.customer.pending_stages())
            if agents:
                self.assign(ev.customer, self.agent_selection_strategy(agents, self.stages))
        customer = self.customer_selection_strategy(ev.agent.stage.name, self.find_available_customers(ev.agent.stage.name))
        if customer:
            self.assign(customer, ev.agent)

    # Handles a single event in the queue. Returns false if the queue is empty.
    def simulate(self):
        if not self.events_queue:
            if self.debug:
                print("All done at t = {}!".format(self.current_time))
            return False, self.current_time
        ev = self.events_queue.pop(0)
        self.current_time = ev.time
        if self.debug:
            print("Fast-forwarded to time = {}".format(self.current_time))
        if (ev.type == "arrived"):
            # Assuming each new customer arrives with all stages pending, let's assign him to any stage for which an agent is available.
            # Assigning fastest/slowest/random stage can be other interesting strategies.
            if self.debug:
                print("customer {} arrived with status {}".format(ev.customer.id, ev.customer.status))

            agents = self.find_available_agents(ev.customer.pending_stages())
            if agents:
                # Assign to the first available agent for that stage.
                # Other strategies (random, performance-based, rewards-based etc) can be considered here.
                self.assign(ev.customer, self.agent_selection_strategy(agents, self.stages))
            else:
                if self.debug:
                    print("customer {} arrived but no agents available".format(ev.customer.id))
                pass
            return True, self.current_time
        elif (ev.type == "serviced"):
            self.release(ev)
            return True, self.current_time
        else:
            print("Unknown event type")
            return False, self.current_time
            
            
