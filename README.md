# SchellingSegregation-Reloaded
This project consists of various models which are adjustments of the original Schelling segregation model. These adjustments are made to investigate the applicability of the Schelling Segregation model when addressed for its assumptions and limitations. Furthermore, these adjustments intend to provide an alternative theory/model for segregation, taking spatial assimilation and place stratification aspects into account. 

## Files explanation
This project contains the following files:

- model1.py: The original Schelling Segregation model, in which a ratio/percentage of homophily is used to determine the satisfaction of an agent and whether it will therefore relocate to a random location
- model2.py: In this model version the original model is adjusted by eliminating the assumption of random relocation. This is done by ensuring that the agents are only able to move to a cell which satisfices their homophily (this changes are implemented under the step function of the Schelling and SchellignAgent class)
- model3a.py: In this model the red and blue agents can only relocate to a cell that is their respective socio-economic "correct" neighborhood. 
- model3b.py: In this model **ONLY** the blue agents can only relocate to a cell that is their respective socio-economic "correct" neighborhood. 

- server.py: Contains the visualisations and setup of the model when launched through a server
- run.py: To run/launch the server for visualisation of the model run
- analysis.ipynb: To (batch) run the different models and experiment and analyse the results
- batch_run.py: Extra file to also batch run the models and save the results to a csv file (for later analysis)

### Changing between models
For both the visualisation of models as the analysis of the models, it is important to note how to change between the models. In both files, one of the first lines of code consists of importing the model (e.g. 'from model2 import Schelling'). Simply change the number to work with the respective model.
Models 3a and 3b differ from the other two models as it requires two or one more parameters respectively. Therefore, when setting up the model run in the analysis.ipynb and batch_run.py, do not forget to add or remove certain parameter values for the respective model. The models require the following parameters:

#### Parameters

- height: of the map/grid (int)
- width: of the map/grid (int)
- density: How densely the grid is populated with agents (float)
- minority_pc: Fraction of the minority (blue agents) in the population 
- homophily: the desired ratio/percentage all agents have for similarity in the neighborhood (8 surrounding cells)

Only Model 3:

- (model3a): socioeconomic_homophily_reds: the percentage of similar agents needed in a neighborhood to deem the cell as a "correct" socio-economic neighborhood
- socioeconomic_homophily_blues ''

For the visualisations of the model (server.py), changing the parameters can be done by adjusting in the ModularServer function (bottom of the file) the last input to model_params1_2, model_params3a or model_params3b, as there will be sliders available in the visualisation.

 