class Agent(object):
    
    def __init__(self, stage, id, x, y):
        self.id = id
        self.stage = stage
        self.available_at = 0
        self.customer = None # all agents are free at the start
        self.position_x = x
        self.position_y = y
    
    def display(self):
        fill("#000000")
        text(self.id, self.position_x+10, self.position_y-10)
        fill(self.stage.color)
        ellipse(self.position_x, self.position_y, 25, 25)
        if self.customer:
            line(self.position_x, self.position_y, self.customer.position_x, self.customer.position_y)
