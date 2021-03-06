import random

class Stage(object):
    
    def __init__(self, name, desc, color, num_agents, servicing_rate, mean_time, seq, depends_on=[]):
        self.name = name
        self.desc = desc
        self.color = color
        self.num_agents = num_agents
        self.servicing_rate = servicing_rate
        self.mean_time = mean_time
        self.seq = seq
        self.depends_on = [] # Not implemented
        
    def servicing_time(self):
        # invoke the servicing_rate lambda
        return self.servicing_rate()
