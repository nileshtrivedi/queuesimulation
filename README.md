# Queue simulation

Queueing theory provides two ways to model and analyze queues: Analytical models and Simulation

See this: http://home.iitk.ac.in/~skb/qbook/Slide_Set_17.PDF

Here, I'm attempting to implement the discrete event time simulation method. In this, we fast forward the system clock to the timestamp when an interesting event (such as arrival or servicing) happens. Processing each event can generate new future events. This is faster and more efficient than continuous time simulation.

I am also in the process of building a visualization of these queueing networks. Hence, using Processing language.

# How To:

- Install Processing IDE: https://processing.org/
- In the top-right of IDE window, you will see a dropdown labeled "Java". Click on it and install the Python mode.
- Open queuesimulation.pyde file in Processing and it will open the entire sketch.
- Running the sketch will show the system state in GUI.
- The nodes on the outside circle are the agents and the ones in the center rectangle are customer.
- Each customer wants to complete 3 stages (color-coded) which are independent of each other.
- We want to be able to model different probability distribution for arrival rate, servicing rate and different allocation strategies such as global first-come-first-serve, random and longest waiting customer within the stage and so on.
- A line drawn between an agent and a customer implies that the agent is currently serving the customer.

# TODO:
- This is not yet complete. Certain edge cases are yet to be handled. However, the basic simulation works with both "Global "