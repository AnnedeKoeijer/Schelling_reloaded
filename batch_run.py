from model2 import Schelling
from datetime import datetime
from random import seed
from mesa import batch_run
import pandas as pd



number_iterations = 100
max_steps_per_simulation = 200

variable_params = {
    "height": 20,
    "width": 20,
    "density": [0.1, 0.2, 0.4, 0.8],
    "minority_pc": [0.1, 0.2, 0.4, 0.8],
    "homophily": [0.1, 0.3, 0.6, 0.7]
}

batchrun = batch_run(
    Schelling,
    variable_params,
    iterations= number_iterations,
    max_steps=max_steps_per_simulation,
)

run_model_data = pd.DataFrame.from_dict(batchrun)

now = str(datetime.now().date())
run_model_data.to_csv("results/model2_data" + now + ".csv")



