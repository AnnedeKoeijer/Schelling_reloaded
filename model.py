from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from random import random
from functions import get_neighbors_snake

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
        for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True,
                                                       radius=1):  # Adjust vision here to Moore (square neighborhood) and radius size
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move to a location within their socioeconomic limits
        if similar < self.model.homophily:
            if self.type == 1:
                if len(self.model.potential_blue_cells) != 0:       # Agent will not move if there are no potential locations left
                    new_location = self.model.random.choice(self.model.potential_blue_cells)
                    self.model.grid.move_agent(self, new_location)
                    self.model.potential_blue_cells.remove(new_location)
                    if new_location in self.model.potential_red_cells:      # Makes sure the new location is removed from both lists
                        self.model.potential_red_cells.remove(new_location)
            else:
                if len(self.model.potential_red_cells) != 0:
                    new_location = self.model.random.choice(self.model.potential_red_cells)
                    self.model.grid.move_agent(self, new_location)
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

    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2, homophily=3, socioeconomic_homophily_reds = 3, socioeconomic_homophily_blues = 5):

        self.total_satisfaction_index = 0
        self.blue_satisfaction_index  = 0
        self.red_satisfaction_index   = 0
        self.total_blue_agents_count  = 0
        self.total_red_agents_count   = 0
        self.happy_blue_agents_count  = 0
        self.happy_red_agents_count   = 0

        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily

        self.socioeconomic_homophily_reds = socioeconomic_homophily_reds    # How many similar agents there must be in a neighborhood to assume it is socioeconomic "correct" neighborhood
        self.socioeconomic_homophily_blues = socioeconomic_homophily_blues
        self.potential_blue_cells = []
        self.potential_red_cells = []

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

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        # Creating the lists including the coordinates of potential locations that are
        # within the socioeconomic limits of the blue (minority) and red (majority) agents
        self.potential_blue_cells = []
        self.potential_red_cells = []
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            if self.grid.is_cell_empty((x,y)):
                list_neighbors = [None, None, None, None, None, None, None, None]
                neighbor_index = 0
                #print(x, y)
                get_neighbors_list = get_neighbors_snake(x,y,self.grid)

                for neighbor in get_neighbors_list:
                    if neighbor == None:
                        neighbor_index += 1
                    else:
                        if neighbor.type == 1:
                            neighbor_index += 1
                            list_neighbors[(neighbor_index - 1)] = 1

                        elif neighbor.type == 0:
                            neighbor_index += 1
                            list_neighbors[(neighbor_index - 1)] = 0

                list2 = list_neighbors.copy()
                list_dubbel = list_neighbors + list2
                #print(list_dubbel)

                #Defining what satisfies as socioeconomic correct neighborhoods
                for i in range(len(list_dubbel) - (self.socioeconomic_homophily_blues - 1)):
                    if all(list_dubbel[i + j] == 1 for j in range(self.socioeconomic_homophily_blues)):
                        #print("This location is for blues")
                        self.potential_blue_cells.append((x, y))
                        break
                if list_neighbors.count(0) <= 1 and list_neighbors.count(1) >= 3:   # ensuring that locations with many similar agents but few empty cells and few majority agents are also added
                    if (x,y) not in self.potential_blue_cells:
                        self.potential_blue_cells.append((x, y))

                for i in range(len(list_dubbel) - (self.socioeconomic_homophily_reds)):
                    if all(list_dubbel[i + j] == 0 for j in range(self.socioeconomic_homophily_reds)):
                        #print("This location is for reds")
                        self.potential_red_cells.append((x, y))
                        break
                if list_neighbors.count(1) <= 6 and list_neighbors.count(0) >= 2:
                    if (x,y) not in self.potential_red_cells:
                        self.potential_red_cells.append((x, y))


        print(f'list of potential locations blues: {self.potential_blue_cells}')
        print(f'list of potential locations reds: {self.potential_red_cells}')



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
