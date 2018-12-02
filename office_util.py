import random

# These functions help us model various types of arrival_rate and servicing_rate models.
# We also provide some strategies for both customer_selection (for "serviced" event) 
# when an agent becomes available and agent selection (for "customer arrived" event)
# when a customer becomes available

# Let's model the arrival rate as a function of time so that probability distributions such as poisson can be modeled
# This is a lambda generator that defines the arrival behaviour.
def all_at_start(period, count):
    # <count> customers come in at the start of every block of <period> seconds
    return lambda current_time: count if (current_time % period == 0) else 0 

# One example of servicing time is where it can vary uniformly randomly between min/max
# These lower and upper bounds for servicing_time are different across stages
# Let's define a lambda generator which can be used as servicing_rate
def uniform_random(min_time, max_time):
    # creates a function that returns a uniformly random value between min & max
    # It's used as servicing_rate for our stages
    return lambda: int(round(min_time + random.random() * (max_time - min_time)))


# We need to experiment with multiple allocation strategies when an agent becomes available
def global_fcfs(stage_name, waiting_customers):
    # Global first-come first-serve policy
    if waiting_customers:
        return waiting_customers[0]
    else:
        return None

def stagewise_fcfs(stage_name, waiting_customers):
    # Give slot to the customer who has been waiting the longest
    if waiting_customers:
        return min(waiting_customers, key=lambda x: x.waiting_since)
    else:
        return None

def random_customer(stage_name, waiting_customers):
    # Give the slot to a randomly selected customer who has this stage as pending
    if waiting_customers:
        return random.sample(waiting_customers, 1)[0]
    else:
        return None

def longest_stage(available_agents, all_stages, randomize=True):
    if randomize:
        return max(random.sample(available_agents, len(available_agents)), key=lambda a: all_stages[a.stage.name].mean_time)
    else:
        return max(available_agents, key=lambda a: all_stages[a.stage.name].mean_time)

def shortest_stage(available_agents, all_stages, randomize=True):
    if randomize:
        return min(random.sample(available_agents, len(available_agents)), key=lambda a: all_stages[a.stage.name].mean_time)
    else:
        return min(available_agents, key=lambda a: all_stages[a.stage.name].mean_time)

def random_agent(available_agents, all_stages):
    return random.sample(available_agents, 1)[0]

def in_stage_sequence(available_agents, all_stages):
    # if all 3 stages are pending, first assign stage 1, then stage 2 & then stage 3
    return min(available_agents, key=lambda a: all_stages[a.stage.name].seq)
