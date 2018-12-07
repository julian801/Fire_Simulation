#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 16:27:08 2018

@author: julianchan
"""
from map_generator import burn_ratio
from Forest_Fire import ForestFire

def total_burn(array_matrix):
    matrix = array_matrix[len(array_matrix) -1] - array_matrix[0] 
    return burn_ratio(matrix)

def run_params():



