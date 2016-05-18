import random
import numpy as np


def getMinTabOf(best_decisions_scores):
    array = np.array(best_decisions_scores)
    return np.amax(array.T, axis=1).tolist()


#return randomly n indice in range n
def get_n_indices_of(n, size_l):
    indices = []
    k = 0
    while k < n :
        r = random.randint(0,size_l-1)
        if(not(r in indices)):
            indices.append(r)
            k += 1

    return indices

#return randomly n element of the list_l
def get_n_elements_of(n, list_l):
    indices = get_n_indices_of(n, len(list_l))
    elements = get_elements_of(indices, list_l)

    return elements

def get_elements_of(indices, list_l):
    elements = (np.array(list_l))[indices]
    return elements
