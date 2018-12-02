import random
import office_util
from stage import Stage
from office import Office

stages = {
    "a": Stage(name="a", desc="document processing"  , color="#ff0000", num_agents=15, servicing_rate=office_util.uniform_random(5*60, 15*60), mean_time=600, seq=1),
    "b": Stage(name="b", desc="police verification"  , color="#00ff00", num_agents=10, servicing_rate=office_util.uniform_random(3*60, 8*60), mean_time=330, seq=2),
    "c": Stage(name="c", desc="biometrics collection", color="#0000ff", num_agents=12, servicing_rate=office_util.uniform_random(5*60, 7*60), mean_time=360, seq=3)
}

num_customers = 180

customer_selection_strategies = [office_util.global_fcfs, office_util.stagewise_fcfs, office_util.random_customer]
agent_selection_strategies = [office_util.longest_stage, office_util.shortest_stage, office_util.random_agent]

for cs in customer_selection_strategies:
    for ags in agent_selection_strategies:
        total_times = []
        per_customer_times = []
        for i in range(10): # simulate each combination 10 times
            office = Office(stages, 
                            arrival_rate=office_util.all_at_start(3600, num_customers),
                            customer_selection_strategy=cs,
                            agent_selection_strategy=ags,
                            enable_gui=False,
                            debug=False)
            
            current_time = 0
            continue_simulate = True
            
            while(continue_simulate):
                continue_simulate, current_time = office.simulate()
            
            # all customers are finished and customer.waiting_since contains their completion timestamp
            avg_processing_time = int(round(sum([(c.waiting_since - c.token_time) for c in office.customers]) / float(num_customers)))
            total_times.append(current_time)
            per_customer_times.append(avg_processing_time)
            print("{},{}: Total time: {} seconds. Avg processing time = {} seconds.".format(cs.func_name, ags.func_name, current_time, avg_processing_time))
        
        avg_total_time = int(round(sum(total_times) / float(10)))
        avg_per_customer_time = int(round(sum(per_customer_times) / float(10)))
        print("Avg Total Time = {}, Avg Processing Time = {}\n".format(avg_total_time, avg_per_customer_time))
