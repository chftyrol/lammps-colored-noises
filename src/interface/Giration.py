#!/usr/bin/env python3

import math , sys
import numpy as np

#Calcola il raggio di girazione delle particelle, dato un file di input dalla fattezza di quelli gir.ecc e ne ritorna il valore
def compute(file):
    
    coord = np.genfromtxt(file, delimiter=" ", skip_header=9, dtype=float)
    Len= len(coord)
    rm = [sum(i) for i in zip(*coord)]
    rm=[rm[0]/Len,rm[1]/Len,rm[2]/Len]
    
    R=0
    for i in range(0,Len):
        R=R+(coord[i][0]-rm[0])**2+(coord[i][1]-rm[1])**2+(coord[i][2]-rm[2])**2
    return(R/Len)

