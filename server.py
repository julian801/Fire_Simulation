#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 19:21:55 2018

@author: julianchan
"""


from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import ForestFire

COLORS = {"Fine": "#00AA00",
          "On Fire": "#880000",
          "Burned Out": "#000000"}


def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.get_pos()
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
tree_chart = ChartModule([{"Label": label, "Color": color} for (label, color) in COLORS.items()])

model_params = {
    "height": 100,
    "width": 100,
    #"border": False,
    #"middle": True,
    "border": UserSettableParameter("slider", "border",1, 0, 1.0, 1),
    "middle": UserSettableParameter("slider", "Box",1, 0, 1.0, 1),
    "margin": UserSettableParameter("slider", "Margin",1, 0, 5, 1),
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01)
}
server = ModularServer(ForestFire, [canvas_element, tree_chart], "Forest Fire", model_params)


