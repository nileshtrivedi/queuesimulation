import bisect
import time
import random

from stage import Stage
from customer import Customer
from agent import Agent
from event import Event

class Office(object):
    
    def __init__(self, stages, arrival_rate, allotment_strategy):
        self.stages = stages
        self.current_time = 0
        self.customers = []
        self.events_queue = []
        self.agents = []
        self.arrival_rate = arrival_rate
        self.allotment_strategy = allotment_strategy

        # new customers arrive in this state (all 3 stages are pending)
        initial_status = {k: "pending" for k, v in stages.items()}
        num_customers = self.arrival_rate(0) # invoking the lambda at t=0
        for i in range(num_customers):
            xpos = 250 + 60*(i % 12)
            ypos = 250 + 50*(i / 12)
            customer = Customer("c{}".format(i), dict(initial_status), xpos, ypos)
            self.customers.append(customer)
            event = Event(type="arrived",agent=None,customer=customer,time=0)
            bisect.insort(self.events_queue, event) # insert in sorting order

        # For each stage, create agents
        for i, s in enumerate(stages.keys()):
            for j in range(stages[s].num_agents):
                agent = Agent(stage=stages[s], id="{}{}".format(s,j), x=300, y=300)
                self.agents.append(agent)
        
        # Arrange all agents in a circle around the waiting area
        # Need to iterate over *all* agents and not stage-wise
        for i, a in enumerate(self.agents):
            a.position = PVector(600+560*cos(i*TAU/len(self.agents)), 600+560*sin(i*TAU/len(self.agents)))

    # Which customers are waiting for the given stage?            
    def find_available_customers(self, sname):
        return [c for c in self.customers if c.agent == None and c.status[sname] == "pending"]
    
    # Which agents are free for the given stages?            
    def find_available_agents(self, stage_names):
        return [a for a in self.agents if a.stage.name in stage_names and a.customer == None]

    # Select an agent to assign
    def select_agent(self, available_agents, randomize=False):
        if randomize:
            return random.shuffle(available_agents)[0]
        else:
            return available_agents[0]

    # Assign a customer to an agent        
    def assign(self, customer, agent):
        customer.status[agent.stage.name] = "ongoing"
        customer.agent = agent
        agent.customer = customer
        agent.available_at = self.current_time + agent.stage.servicing_time()
        print("assigning {} to {} till {}".format(customer.id, agent.id, agent.available_at))
        new_event = Event(type="serviced",agent=agent,customer=customer,time=agent.available_at)
        bisect.insort(self.events_queue, new_event) # insert in the right order
        
    # Process servicing completed event
    def release(self, ev):
        print("releasing {} from {}".format(ev.customer.id, ev.agent.id))
        ev.agent.customer = None
        ev.customer.status[ev.agent.stage.name] = "done"
        ev.customer.agent = None
        if ev.customer.is_finished(self.stages.keys()):
            print("customer {} is finished".format(ev.customer.id))
            #self.customers.remove(ev.customer)
        else:
            agents = self.find_available_agents(ev.customer.pending_stages())
            if agents:
                self.assign(ev.customer, self.select_agent(agents))
        customer = self.allotment_strategy(ev.agent.stage.name, self.find_available_customers(ev.agent.stage.name))
        if customer:
            self.assign(customer, ev.agent)

    def simulate(self):
        # time.sleep(0.5)
        if not self.events_queue:
            print("All done!")
            return False
        ev = self.events_queue.pop(0)
        if (ev.type == "arrived"):
            # Assuming each new customer arrives with all stages pending, let's assign him to any stage for which an agent is available.
            # Assigning fastest/slowest/random stage can be other interesting strategies.
            print("customer {} arrived with {} pending".format(ev.customer.id, ev.customer.status))
            agents = self.find_available_agents(ev.customer.pending_stages())
            if agents:
                # Assign to the first available agent for that stage.
                # Other strategies (random, performance-based, rewards-based etc) can be considered here.
                self.assign(ev.customer, self.select_agent(agents))
            else:
                print("customer {} arrived but no agents available".format(ev.customer.id))
                pass
            return True
        elif (ev.type == "serviced"):
            self.release(ev)
            return True
        else:
            print("Unknown event type")
            return False
            
            
