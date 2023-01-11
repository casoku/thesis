import matplotlib.pyplot as plt

def pareto_graph(paths):

    x = []
    y = []

    for path in paths:
        x.append(path["cost"])
        y.append(path["probability"])


    plt.xlabel("Cost (# of steps)", fontsize = 14)
    plt.ylabel("Success probability", fontsize = 14)
    plt.tick_params(labelsize = 14)
    plt.scatter(x, y, c ="blue")
    plt.tight_layout()
    
    # To show the plot
    plt.show()

