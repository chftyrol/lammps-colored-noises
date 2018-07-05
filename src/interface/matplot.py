#!/usr/bin/env python3

import matplotlib.pyplot as plt

def plot(X,Y):

    #scatter plot
    plt.scatter(X, Y, s=60, c='blue', marker='o')

    #change axes ranges
    #plt.xlim(0,1000)
#plt.ylim(0,100)

    #add title
    plt.title('Radius of gyration of the particle system')

    #add x and y labels
    plt.xlabel('Timestep')
    plt.ylabel('Rg')

    #show plot
    plt.show()
