import matplotlib.pyplot as plt

def pareto_graph(paths):

    x = []
    y = []

    for path in paths:
        x.append(path["cost"])
        y.append(path["probability"])


    plt.xlabel("Cost (# of steps)")
    plt.ylabel("Success probability (%)")
    plt.scatter(x, y, c ="blue")
    plt.tight_layout()
    
    # To show the plot
    plt.show()

