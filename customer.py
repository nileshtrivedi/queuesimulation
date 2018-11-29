class Customer(object):
    
    def __init__(self, id, status, x, y):
        self.id = id
        self.status = status
        self.waiting_since = 0
        self.available_at = 0
        self.position = PVector(x, y)
        self.agent = None
        
    def is_finished(self, stage_names):
        for sname in stage_names:
            if(self.status[sname] != "done"):
                return False
        return True
    
    def pending_stages(self):
        return [sname for sname in self.status.keys() if self.status[sname] == "pending"]
        
    def display(self, stages):
        fill("#000000")
        text(self.id, self.position.x+10, self.position.y-10)
        for i, sname in enumerate(stages.keys()):
            if self.status[sname] == "done":
                fill(stages[sname].color)
            else:
                fill(200)
            arc(self.position.x, self.position.y, 30, 30, i*TAU/len(stages.keys()), (i+1)*TAU/len(stages.keys()), PIE)
