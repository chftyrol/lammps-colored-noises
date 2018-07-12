import matplotlib.pyplot as plt

#given two vectors for axes coordinates, generates a scatterplot
def plot(X,Y):

    #scatter plot
    plt.scatter(X, Y, s=60, c='blue', marker='o')

    #change axes ranges
    #plt.xlim(0,1000)
    #plt.ylim(0,100)

    #add title
    plt.title('Radius of gyration of the particle system')

    #add x and y labels
    plt.xlabel('Timestep[t_unit]')
    plt.ylabel('Rg[l_unit^2]')

    #show plot
    plt.show()
