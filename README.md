# SchellingSegregation-Reloaded
This project consists of various models which are adjustments of the original Schelling segregation model. These adjustments are made to investigate the applicability of the Schelling Segregation model when addressed for its assumptions and limitations. Furthermore, these adjustments intend to provide an alternative theory/model for segregation, taking spatial assimilation and place stratification aspects into account. 

## Files explanation
This project contains the following files:

- model1.py: The original Schelling Segregation model, in which a ratio/percentage of homophily is used to determine the satisfaction of an agent and whether it will therefore relocate to a random location
- model2.py: In this model version the original model is adjusted by eliminating the assumption of random relocation. This is done by ensuring that the agents are only able to move to a cell which satisfices their homophily (this changes are implemented under the step function of the Schelling and SchellignAgent class)
- model3.py: In this model the agents can only relocate to a cell that is their respective socio-economic "correct" neighborhood. 

- server.py: Contains the visualisations and setup of the model when launched through a server
- run.py: To run/launch the server
- analysis:.ipynb To experiment and analyse the results of the different models
- batch_run.py: -(ignore for now)

### Changing between models
For both the visualisation of models as the analysis of the models, it is important to note how to change between the models. In both files, one of the first lines of code consists of importing the model (e.g. 'from model2 import Schelling'). Simply change the number to work with the respective model.
Model 3 differs from the other two models as it requires two more parameters. The models require the following parameters:

- height: of the map/grid (int)
- width: of the map/grid (int)
- density: How densely the grid is populated with agents (float)
- minority_pc: Fraction of the minority (blue agents) in the population 
- homophily: the desired ratio/percentage all agents have for similarity in the neighborhood (8 surrounding cells)

Only Model 3:

- socioeconomic_homophily_reds: the percentage of similar agents needed in a neighborhood to deem the cell as a "correct" socio-economic neighborhood
- socioeconomic_homophily_blues ''

For the visualisations (file) of the model, changing the parameters can be done by adjusting in the ModularServer function (bottom of the file) the last input to model_params1_2 or model_params3, as there will eb sliders available in the visualisation.

 