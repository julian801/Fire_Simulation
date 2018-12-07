#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Title: Project Mesa ForestFire Example
 Authors: Project Mesa, Wilensky, U. (1997). NetLogo Fire model. http://ccl.northwestern.edu/netlogo/models/Fire. 
 Availability: https://github.com/projectmesa/mesa-examples/tree/master/examples/ForestFire
 My personal use: Apapted this program to change some of the parameters and interact with 
 a folium map.
"""
# Code review: Kristian 2018/12/02


import numpy as np
import random
import matplotlib.pyplot as plt
import math
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner


class TreeCell(Agent):
    '''
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good practice to give one to each
    agent anyway.
    '''
    # KR: reference your source for the model you adapted

    def __init__(self, model, pos):
        '''
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid. Used as the unique_id
        '''
        super().__init__(pos, model)
        self.pos = pos
        self.unique_id = pos
        self.condition = "Fine"

    def step(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        '''
        # KR: this is an example of a great docstring
        if self.condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
            for neighbor in neighbors:
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"

# End of class
# KR: this comment is redundant and should be removed

class ForestFire(Model):
    '''
    Simple Forest Fire model.
    '''
    import random
    # KR: import is already on top

    def __init__(self, height, width, density):
        '''
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        self.MatrixHistory = []
        self.matrix = np.zeros((width, height))
        # Initialize model parameters
        self.height = height
        self.width = width
        self.density = density

        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)
        self.dc = DataCollector({"Fine": lambda m: self.count_type(m, "Fine"),
                                 "On Fire": lambda m: self.count_type(m, "On Fire"),
                                 "Burned Out": lambda m: self.count_type(m, "Burned Out")})

        # Place a tree in each cell with Prob = density
        for x in range(self.width):
            for y in range(self.height):
                if self.random.random() < self.density:
                    # Create a tree
                    new_tree = TreeCell(self, (x, y))
                    # Set all trees in the first column on fire.
                    # Edit below to change the location of the fire <--------------------------
                    if x == 0:
                        new_tree.condition = "On Fire"
                    self.grid[y][x] = new_tree
                    # Edits below ----------------------------------
                    if new_tree.condition == "On Fire":
                        self.matrix[x][y] = 1
                    if new_tree.condition == "Burned Out":
                        self.matrix[x][y] = 1
                    if new_tree.condition == "Fine":
                        self.matrix[x][y] = 0
                    self.schedule.add(new_tree)
        self.running = True
        # print(self.matrix)

    def step(self):
        '''
        Advance the model by one step.
        '''
        self.schedule.step()
        self.dc.collect(self)
        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        '''
        Helper method to count trees in a given condition in a given model.
        '''
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
            if tree.condition == "Burned Out":
                model.matrix[tree.pos[0]][tree.pos[1]] = 1
            if tree.condition == "On Fire":
                model.matrix[tree.pos[0]][tree.pos[1]] = 1
            model.MatrixHistory.append(model.matrix.copy())
        return count
# End of class

#fire = ForestFire(4+1, 20+1, 0.5)
# fire.run_model()

# KR: remove last three comments
