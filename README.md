# Passport office problem

Here, I've implemented the discrete event time simulation method for analyzing a queueing network. In this, we fast forward the system clock to the timestamp when an interesting event (such as arrival or servicing) happens. Processing each event can generate new future events. This is faster and more efficient than continuous time simulation.

I have also built a visualization of these queueing networks using Processing framework. Please check recording.mov file for a demo run. 

The actual system evolution is implemented in office.py and the system setup is in queuesimulation.pyde

# Assumptions

The provided problem statement was unclear about certain key aspects. The serving rate for token allocation wasn't specified. The problem description is ambiguous about stages being independent.
I assumed that generating token number has a single agent and takes 1 second without any variance. I assumed that tasks are independent and if a customer has all 3 stages pending, and if an agent for stage 2 or 3 becomes available, this customer will be processed immediately instead of both the customer and agent being idle.

# How To:

- Install Processing IDE: https://processing.org/
- In the top-right of IDE window, you will see a dropdown labeled "Java". Click on it and install the Python mode.
- Open queuesimulation.pyde file in Processing and it will open the entire sketch.
- Running the sketch will show the system state in GUI.
- The nodes on the outside circle are the agents and the ones in the center rectangle are customer.
- Each customer wants to complete 3 stages (color-coded) which are independent of each other.
- We want to be able to model different probability distribution for arrival rate, servicing rate and different allocation strategies such as global first-come-first-serve, random and longest waiting customer within the stage and so on.
- A line drawn between an agent and a customer implies that the agent is currently serving the customer.
- To run the benchmarks for various queueing disciplines, use `python bench.py`

# Results
```
+----------------------------+-------------------------+----------------------------------------------+--------------------------------------------+
| CustomerAllocationStrategy | AgentAllocationStrategy | Average Processing Time / Customer (seconds) | Average # of applications processed / Hour |
+----------------------------+-------------------------+----------------------------------------------+--------------------------------------------+
| Global FCFS                | LongestStage            |                                         3934 |                                       85.1 |
| Global FCFS                | ShortestStage           |                                         3954 |                                       84.8 |
| Global FCFS                | RandomAgent             |                                         3881 |                                       86.1 |
| Stagewise FCFS             | LongestStage            |                                         5342 |                                       85.2 |
| Stagewise FCFS             | ShortestStage           |                                         5364 |                                       84.6 |
| Stagewise FCFS             | RandomAgent             |                                         5342 |                                       85.7 |
| Random                     | LongestStage            |                                         4973 |                                       85.7 |
| Random                     | ShortestStage           |                                         4996 |                                       85.9 |
| Random                     | RandomAgent             |                                         4941 |                                       86.0 |
+----------------------------+-------------------------+----------------------------------------------+--------------------------------------------+

```
