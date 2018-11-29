class Event(object):
    
    def __init__(self, type, agent, customer, time):
        self.type = type
        self.agent = agent
        self.customer = customer
        self.time = time

    def __lt__(a,b):
        return a.time < b.time
    
    def __gt__(a,b):
        return a.time > b.time
