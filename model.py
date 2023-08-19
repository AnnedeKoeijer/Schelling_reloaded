from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from random import random

class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, pos, model, agent_type):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.friends = []

    def step(self):
        similar = 0
        for neighbor in self.model.grid.iter_neighbors(self.pos, moore = True, radius = 1):    #Adjust vision here to Moore (square neighborhood) and radius size
            if neighbor.type == self.type:
                similar += 1


        # If unhappy, move
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        # Count happy agents
        else:
            self.model.happy += 1
            if self.type == 1:
                self.model.happy_blue_agents_count += 1
            else:
                self.model.happy_red_agents_count += 1


class Schelling(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2, homophily=3):

        self.total_satisfaction_index = 0 # o indice total de agentes satisfeitos
        self.blue_satisfaction_index  = 0 # o indice de agentes azuis satisfeitos
        self.red_satisfaction_index   = 0 # o indice de agentes vermelhos satisfeitos
        self.total_blue_agents_count  = 0 # o total de agentes azuis
        self.total_red_agents_count   = 0 # o total de agentes vermelhos
        self.happy_blue_agents_count  = 0 # o numero de agentes azuis felizes
        self.happy_red_agents_count   = 0 # o numero de agentes vermelhos felizes

        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.happy = 0
        self.datacollector = DataCollector(
            {
                "happy": "happy",
                "total_satisfaction_index": lambda m: self.total_satisfaction_index,
                "blue_satisfaction_index": lambda m: self.blue_satisfaction_index,
                "red_satisfaction_index": lambda m: self.red_satisfaction_index,
            },
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                    self.total_blue_agents_count += 1
                else:
                    agent_type = 0
                    self.total_red_agents_count += 1
                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, x, y)
                self.schedule.add(agent)

                #Create friends of agent
                #for i in range(4): #Number of friends an individual has
                 #   friend = self.random.choice(self.schedule.agents)
                  #  if friend != self and friend not in agent.friends:
                   #     agent.friends.append(friend)
                    #    friend.friends.append(self)     #make sure they are in each others friend list


        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """

        # calculates the blue and red satisfaction index
        self.blue_satisfaction_index = float(self.happy_blue_agents_count / max(self.total_blue_agents_count, 1))
        self.red_satisfaction_index  = float(self.happy_red_agents_count / max(self.total_red_agents_count, 1))
        
        # calculates the total satisfaction index
        total_agents = self.total_blue_agents_count + self.total_red_agents_count
        happy_agents = self.happy_blue_agents_count + self.happy_red_agents_count
        self.total_satisfaction_index = float(happy_agents / total_agents)

        self.happy = 0  # Reset counter of happy agents
        self.happy_blue_agents_count = 0
        self.happy_red_agents_count = 0
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False






