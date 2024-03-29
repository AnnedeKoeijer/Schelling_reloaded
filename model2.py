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
           agent_type: Indicator for the agent's type (minority=1 (blue), majority=0 (red))
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        total_neighbors = 0
        for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True,
                                                       radius=1):  # Adjust vision here to Moore (square neighborhood) and radius size
            total_neighbors += 1
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move to a location within their socioeconomic limits
        if total_neighbors == 0 or ((similar / total_neighbors) < self.model.homophily):
            if self.type == 1:
                if len(self.model.potential_blue_cells) != 0:  # Agent will not move if there are no potential locations left
                    new_location = self.model.random.choice(self.model.potential_blue_cells)
                    self.model.grid.move_agent(self, new_location)
                    self.model.movements += 1
                    self.model.potential_blue_cells.remove(new_location)
                    if new_location in self.model.potential_red_cells:  # Makes sure the new location is removed from both lists
                        self.model.potential_red_cells.remove(new_location)
            else:
                if len(self.model.potential_red_cells) != 0:
                    new_location = self.model.random.choice(self.model.potential_red_cells)
                    self.model.grid.move_agent(self, new_location)
                    self.model.movements += 1
                    self.model.potential_red_cells.remove(new_location)
                    if new_location in self.model.potential_blue_cells:
                        self.model.potential_blue_cells.remove(new_location)


        # Otherwise count agent as happy
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

        self.total_satisfaction_index = 0
        self.blue_satisfaction_index = 0
        self.red_satisfaction_index = 0
        self.total_blue_agents_count = 0
        self.total_red_agents_count = 0
        self.happy_blue_agents_count = 0
        self.happy_red_agents_count = 0

        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily

        self.potential_blue_cells = []
        self.potential_red_cells = []

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        #to count per step the amount of agents that have relocated
        self.movements = 0

        self.time =0

        self.happy = 0
        self.happiness_reached = False

        self.datacollector = DataCollector(
            {
                "happy": "happy",
                "total_satisfaction_index": lambda m: self.total_satisfaction_index,
                "blue_satisfaction_index": lambda m: self.blue_satisfaction_index,
                "red_satisfaction_index": lambda m: self.red_satisfaction_index,
                "segregated_Agents": get_segregation,
                "happiness reached" : "happiness_reached"
            }
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1][0]
            y = cell[1][1]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                    self.total_blue_agents_count += 1
                else:
                    agent_type = 0
                    self.total_red_agents_count += 1
                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.place_agent(agent=agent, pos=(x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

        print("This is model 2")

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        # Stop the model when everyone is not moving anymore due to happiness or due to lack of movement
        if self.movements == 0 and self.schedule.time >0:
            self.running = False

        # Creating the lists including the coordinates of potential locations that are
        # within the socioeconomic limits of the blue (minority) and red (majority) agents
        self.potential_blue_cells = []
        self.potential_red_cells = []
        for cell in self.grid.coord_iter():
            x = cell[1][0]
            y = cell[1][1]

            if self.grid.is_cell_empty((x, y)):
                list_neighbors = []
                get_neighbors_list = self.grid.get_neighbors((x, y), moore=True, radius=1)

                for neighbor in get_neighbors_list:
                    if neighbor.type == 1:
                        list_neighbors += [1]

                    elif neighbor.type == 0:
                        list_neighbors += [0]

                # Defining what satisfies as homophily correct neighborhoods
                if ((list_neighbors.count(0) + list_neighbors.count(1)) != 0) and (
                (list_neighbors.count(1) / (list_neighbors.count(0) + list_neighbors.count(1)))) >= self.homophily:
                    if (x, y) not in self.potential_blue_cells:
                        self.potential_blue_cells.append((x, y))

                if ((list_neighbors.count(0) + list_neighbors.count(1)) != 0) and (
                (list_neighbors.count(0) / (list_neighbors.count(0) + list_neighbors.count(1)))) >= self.homophily:
                    if (x, y) not in self.potential_red_cells:
                        self.potential_red_cells.append((x, y))

        #print(f'list of potential locations blues: {self.potential_blue_cells}')
        #print(f'list of potential locations reds: {self.potential_red_cells}')


        self.happy = 0  # Reset counter of happy agents
        self.happy_blue_agents_count = 0
        self.happy_red_agents_count = 0
        self.movements = 0
        self.schedule.step()

        self.time = self.schedule.time

        # calculates the blue and red satisfaction index
        self.blue_satisfaction_index = float(self.happy_blue_agents_count / max(self.total_blue_agents_count, 1))
        self.red_satisfaction_index = float(self.happy_red_agents_count / max(self.total_red_agents_count, 1))

        # calculates the total satisfaction index
        total_agents = self.total_blue_agents_count + self.total_red_agents_count
        happy_agents = self.happy_blue_agents_count + self.happy_red_agents_count
        self.total_satisfaction_index = float(happy_agents / total_agents)

        if self.happy == self.schedule.get_agent_count():
            self.happiness_reached = True
        # collect data
        self.datacollector.collect(self)


#Function that defines when an agent is segregated (for Datacollector)
def get_segregation(model):
    '''
    Find the % of agents that only have neighbors of their same type.
    '''
    segregated_agents = 0
    for agent in model.schedule.agents:
        segregated = True
        for neighbor in model.grid.iter_neighbors(agent.pos, moore=True):
            if neighbor.type != agent.type:
                segregated = False
                break
        if segregated:
            segregated_agents += 1
    return segregated_agents / model.schedule.get_agent_count()