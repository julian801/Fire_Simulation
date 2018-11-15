#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 22:45:54 2018

@author: julianchan
"""
# server.py
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import MoneyModel
import numpy as np


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"
    def render(self, model):
        wealth_vals = [agent.wealth for agent in model.schedule.agents]
        hist = np.histogram(wealth_vals, bins=self.bins)[0]
        return [int(x) for x in hist]
    
###NOT PAT OF THE CLASS

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.wealth > 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal



grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)


n_slider = UserSettableParameter('slider', "Number of Agents", 100, 2, 200, 1)

chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(MoneyModel,
                       [grid, chart],
                       "Money Model",
                       {"N": n_slider, "width": 10, "height": 10})


###Uncomment below for JS histogram-------

#histogram = HistogramModule(list(range(10)), 200, 500)
#server = ModularServer(MoneyModel,
#                       [grid, histogram, chart],
#                       "Money Model",
#                       {"N": n_slider, "width": 10, "height": 10})


