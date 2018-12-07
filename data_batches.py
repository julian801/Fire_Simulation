#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 16:27:08 2018

@author: julianchan
"""
from Forest_Fire import ForestFire

def run_n_times(n,length, density, border, middle, margin):
    data = []
    for i in range(0,n):
        fire = ForestFire(length, length, density, border, middle, margin)
        fire.run_model()
        matrix = fire.MatrixHistory[len(fire.MatrixHistory) -1] - fire.MatrixHistory[0]
        burn = matrix.sum()/(matrix.shape[0]*matrix.shape[1])
        data.append([density, burn, border, middle, margin])
    return data

def data_density(n,length, density, border, middle, margin):
    density_data = []
    for p in density:
        for i in range(0,n):
            fire = ForestFire(length, length, p, border, middle, margin)
            fire.run_model()
            matrix = fire.MatrixHistory[len(fire.MatrixHistory) -1] - fire.MatrixHistory[0]
            burn = matrix.sum()/(matrix.shape[0]*matrix.shape[1])
            density_data.append([p, burn, border, middle, margin])
    return density_data

def data_border(n,length, density):
    border_data = []
    for p in density:
        for i in range(0,n):
            fire = ForestFire(length, length, p, True, False, 0)
            fire.run_model()
            matrix = fire.MatrixHistory[len(fire.MatrixHistory) -1] - fire.MatrixHistory[0]
            burn = matrix.sum()/(matrix.shape[0]*matrix.shape[1])
            border_data.append([p, burn])
    return border_data        

def data_middle(n,length, density, margin):
    middle_data = []
    for m in margin:
        for p in density:    
            for i in range(0,n):
                fire = ForestFire(length, length, p, False, True, m)
                fire.run_model()
                matrix = fire.MatrixHistory[len(fire.MatrixHistory) -1] - fire.MatrixHistory[0]
                burn = matrix.sum()/(matrix.shape[0]*matrix.shape[1])
                middle_data.append([p, burn, m])
    return middle_data  



