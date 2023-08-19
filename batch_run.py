from model import Schelling
from mesa.batchrunner import BatchRunner
from datetime import datetime
from random import seed

def happy(model):
    return model.happy
def density(model):
    return model.density
def minority_pc(model):
    return model.minority_pc
def homophily(model):
    return model.homophily

def total_satisfaction_index(model):
    return model.total_satisfaction_index
def blue_satisfaction_index(model):
    return model.blue_satisfaction_index
def red_satisfaction_index(model):
    return model.red_satisfaction_index


def batch_run():
    # a tolerancia e fixada para testar seus efeitos no modelo, principalmente sobre a
    # variavel total satisfaction index e blue/red satisfaction index
    number_iterations = 200
    max_steps_per_simulation = 200

    fixed_params = {
        "height": 20,
        "width": 20,
    }
    # densidade, fracao da minoria e homofilia sao testadas em intervalos de 4
    variable_params = {
        "density": [0.1, 0.2, 0.4, 0.8],
        "minority_pc": [0.1, 0.2, 0.4, 0.8],
        "homophily": [1, 3, 6, 7]
    }

    batch_run = BatchRunner(
        Schelling,
        variable_params,
        fixed_params,
        iterations=number_iterations,
        max_steps=max_steps_per_simulation,
        model_reporters={
            "Density": density,
            "MinorityPC": minority_pc,
            "Homophily": homophily,
            "HappyAgents": happy,
            "TotalSatisfactionIndex": total_satisfaction_index,
            "BlueSatisfactionIndex": blue_satisfaction_index,
            "RedSatisfactionIndex": red_satisfaction_index,
        },
        agent_reporters={
            "Position": "pos",
            "AgentType": "type",
        }
    )
    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    run_agent_data = batch_run.get_agent_vars_dataframe()

    now = str(datetime.now().date())
    run_model_data.to_csv("results/model_data" + now + ".csv")
    run_agent_data.to_csv("results/agent_data" + now + ".csv")

# uncomment to collect the data and generate the .csv
# batch_run()