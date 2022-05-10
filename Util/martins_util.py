from numpy import Infinity


def order_lexicographically(labels):
    sorted_lables = sorted(labels,
                         key=lambda x: (1-x.probability, x.cost))
    
    return sorted_lables