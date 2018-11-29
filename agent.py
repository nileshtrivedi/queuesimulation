class Agent(object):
    
    def __init__(self, stage, id, x, y):
        self.id = id
        self.stage = stage
        self.available_at = 0
        self.customer = None # all agents are free at the start
        self.position = PVector(x, y)
    
    def display(self):
        fill("#000000")
        text(self.id, self.position.x+10, self.position.y-10)
        fill(self.stage.color)
        ellipse(self.position.x, self.position.y, 25, 25)
        if self.customer:
            line(self.position.x, self.position.y, self.customer.position.x, self.customer.position.y)
