import random
from stage import Stage
from office import Office

# This simulation is an event queue where processing each event can create future events.
# We process the first event and insert any new events generated at the right place in queue.
# Once the queue is empty, we're done!
# This way, we can fast-forward to future where an interesting event happens.
# This ensures that simulation finishes quickly.
# Interesting events for us are when either a customer or an agent becomes available.
# Hence, two event types: "arrived" and "serviced".


# This is a discrete simulation and so, we will model time in integer seconds
# We want to support arbitrary probability distributions for arrival_rate and servicing_rate
# Hence, we will use lambdas to model both of these.

# One example of servicing time is where it can vary uniformly randomly between min/max
# These lower and upper bounds for servicing_time are different across stages
# Let's define a lambda generator which can be used as servicing_rate
def uniform_random(min_time, max_time):
    # creates a function that returns a uniformly random value between min & max
    # It's used as servicing_rate for our stages
    return lambda: int(round(min_time + random.random() * (max_time - min_time)))


# Define the stages, the number of agents serving each stage, the servicing_time probability distribution.
# Dependencies between stages are currently not implemented.
stages = {
    "a": Stage(name="a", desc="document processing"  , color="#ff0000", num_agents=15, servicing_rate=uniform_random(5*60, 15*60)),
    "b": Stage(name="b", desc="police verification"  , color="#00ff00", num_agents=10, servicing_rate=uniform_random(3*60, 8*60)),
    "c": Stage(name="c", desc="biometrics collection", color="#0000ff", num_agents=12, servicing_rate=uniform_random(5*60, 7*60))
}

# Let's model the arrival rate as a function of time so that probability distributions such as poisson can be modeled
# This is a lambda generator that defines the arrival behaviour.
def all_at_start(period, count):
    # <count> customers come in at the start of every block of <period> seconds
    return lambda current_time: count if (current_time % period == 0) else 0 


# We need to experiment with multiple allocation strategies when an agent becomes available
def global_fcfs(sname, waiting_customers):
    # Global first-come first-serve policy
    if waiting_customers:
        return waiting_customers[0]
    else:
        return None

def stagewise_fcfs(sname, waiting_customers):
    # Give slot to the customer who has been waiting the longest
    return None #TODO

def random_allocation(sname, waiting_customers):
    # Give the slot to a randomly selected customer who has this stage as pending
    if waiting_customers:
        return random.sample(waiting_customers, 1)[0]
    else:
        return None

office = Office(stages, arrival_rate=all_at_start(3600, 180), allotment_strategy=random_allocation)
continue_simulate = True

def setup():
    size(1200, 1200)
    font = createFont("Arial",16,True)
    textFont(font)
    print("starting...")

def draw():
    global continue_simulate
    background(200,200,200)
    for c in office.customers:
        c.display(office.stages)
    for a in office.agents:
        a.display()

    if continue_simulate:
        continue_simulate = office.simulate()
