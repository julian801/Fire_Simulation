#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 16:05:06 2018

@author: julianchan
"""
# run.py
from server import server
from mesa.batchrunner import BatchRunner
from model import MoneyModel
import numpy as np
import matplotlib.pyplot as plt



model = MoneyModel(50, 10, 10)
for i in range(20):
    model.step()

agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()

# If running from a text editor or IDE, remember you'll need the following:
plt.show()

gini = model.datacollector.get_model_vars_dataframe()
gini.plot()
plt.close
##Agent wealth data
agent_wealth = model.datacollector.get_agent_vars_dataframe()
agent_wealth.head()

plt.show()
one_agent_wealth = agent_wealth.xs(14, level="AgentID")
one_agent_wealth.Wealth.plot()

##Batch runner
fixed_params = {"width": 10,
                "height": 10}
variable_params = {"N": range(10, 500, 10)}

batch_run = BatchRunner(MoneyModel,
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=5,
                        max_steps=100,
                        model_reporters={"Gini": compute_gini})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)

###Server for visualization
server.port = 8521 # The default
server.launch()


