import random
import math
import numpy


########################################################################
# Objective functions
########################################################################
def getObjectives():
    return [f1, f2]

def getFrontPareto():
    tf1 = []
    tf2 = []
    tmp = 0.001
    for i in range(1000):
        tf1.append(tmp)
        tmp += 0.001
    tf2 = [1 - tf1[i] for i in range(1000)]

    return tf1, tf2



def getProblemTitle():
    return "Unconstrained Problem 7"

def getSearchSpace(problem_size):
    search_space = [[1,(0,1)], [problem_size-1, (-1,1)]]
    return search_space


#FAIRE ATTENTION A PAIRE ET IMPAIRE : il y a un decalage
def f1(x_vector, vector_size):
    global N, epsilon

    decalage = 1
    nb_odd = (vector_size-1) // 2

    x_1 = x_vector[1 - decalage]

    tmp1 = math.pow(x_1, 1.0/ 5.0)

    tmp2 = 2.0 / abs(nb_odd)

    sum_y = 0
    for odd in range(1 + decalage, vector_size, 2):
        sum_y     += y_function(x_1, x_vector[odd], odd ,vector_size)**2

    return tmp1 + tmp2 * sum_y






def y_function(x_1, x_j, j, n):
    return x_j - math.sin(6 * math.pi * x_1 + ((j * math.pi) / float(n)))



#return number of '0' in a binary string
def f2(x_vector, vector_size):
    global N, epsilon

    decalage = 1
    nb_even = (vector_size-1) // 2 + ((vector_size-1)%2)

    x_1 = x_vector[1 - decalage]

    tmp1 = math.pow(x_1, 1.0/ 5.0)

    tmp2 = 2.0 / abs(nb_even)

    sum_y = 0
    for even in range(0 + decalage, vector_size, 2):
        sum_y     += y_function(x_1, x_vector[even], even ,vector_size)**2

    return 1 - tmp1 + tmp2 * sum_y
