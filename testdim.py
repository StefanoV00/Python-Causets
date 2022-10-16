#!/usr/bin/env python
"""
Created on 13 Oct 2022

@author: Stefano Veroni
"""
#%%
from __future__ import annotations
from typing import List, Tuple 

from causets.causetevent import CausetEvent
from causets.causet import Causet
from causets.sprinkledcauset import SprinkledCauset
from causets.shapes import CoordinateShape
from causets.spacetimes import *
import causets.causetplotting as cplt


import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

st   = [FlatSpacetime, deSitterSpacetime, 
       AntideSitterSpacetime, BlackHoleSpacetime]
dims = [  [1,2,3,4],       [2,3,4],            
           [2,3,4],          [2]       ]

#%% CHECK DIMESNION ESTIMATOR IN FLAT SPACETIME FOR ALL COORDINATES
Ns = [128, 96, 64, 32, 16]
radius = 5
dim_est = []
dim_std = []
for i in range(len(dims[0])):
    d = dims[0][i]
    dim_est.append([])
    dim_std.append([])
    S: CoordinateShape = CoordinateShape(d, 'cylinder', radius = radius,
                                        duration=10, hollow=1)
    C: SprinkledCauset = SprinkledCauset(card=Ns[0],
                                        spacetime=FlatSpacetime(d), 
                                        shape=S)
    for n in tqdm(Ns, f"Dimension {d}"):
        C.coarsegrain(card = cut)
        MMd = C.MMdim_est(Nsamples = 20, 
                            ptime_constr=lambda t:t<2*radius,
                            size_min = min(20, int(N0/2)))
        dim_est[i].append(MMd[0]) 
        dim_std[i].append(MMd[1])     
# %%
plt.figure("MMFlatDim")
for i in range(len(dims[0])):
    plt.errorbar(Ns.sort(reverse = 1), dim_est[i].sort(reverse = True), 
                    yerr = dim_std[i].sort(reverse = True),
                    fmt = ".", capsize = 4, label = f"Dimension {dims[0][i]}")
plt.title("Testing Myrheim-Mayers Estimator in Minkowski")
plt.xlabel("Cardinality")
plt.ylabel("Dimension")