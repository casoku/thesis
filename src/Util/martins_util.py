def order_lexicographically(labels):
    sorted_lables = sorted(labels,
                         key=lambda x: (1-x.probability, x.cost))
    
    return sorted_lables

def order_lexicographically_dict(labels):
    sorted_lables = sorted(labels,
                         key=lambda x: (1-x['probability'], x['cost']))
    
    return sorted_lables