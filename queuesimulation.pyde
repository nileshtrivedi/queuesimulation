import time
import random
import office_util
from stage import Stage
from office import Office

# Define the stages, the number of agents serving each stage, the servicing_time probability distribution.
# Dependencies between stages is pending but will be trivial to implement in the strategies
stages = {
    "a": Stage(name="a", desc="document processing"  , color="#ff0000", num_agents=15, servicing_rate=office_util.uniform_random(5*60, 15*60), mean_time=600, seq=1),
    "b": Stage(name="b", desc="police verification"  , color="#00ff00", num_agents=10, servicing_rate=office_util.uniform_random(3*60, 8*60), mean_time=330, seq=2),
    "c": Stage(name="c", desc="biometrics collection", color="#0000ff", num_agents=12, servicing_rate=office_util.uniform_random(5*60, 7*60), mean_time=360, seq=3)
}

office = Office(stages,
                arrival_rate=office_util.all_at_start(3600, 180),
                customer_selection_strategy=office_util.stagewise_fcfs,
                agent_selection_strategy=office_util.longest_stage,
                enable_gui=True,
                debug=True)

continue_simulate = True

def setup():
    size(1200, 1200)
    font = createFont("Arial",16,True)
    textFont(font)
    print("starting at t = 0")

def draw():
    global continue_simulate
    background(200,200,200)
    for c in office.customers:
        c.display(office.stages)
    for a in office.agents:
        a.display()
    text("t = {}".format(office.current_time), 20, 20)

    if continue_simulate and not mousePressed:
        continue_simulate, timestamp = office.simulate()
        time.sleep(0.3)
