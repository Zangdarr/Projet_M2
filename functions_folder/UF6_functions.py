import random
import math
import numpy

########################################################################
# Parameters from CEC'09
########################################################################
N = 2
epsilon = 0.1

########################################################################
# Objective functions
########################################################################

def getFrontPareto():
    global N

    point_by_part = 1000// N

    tf1 = [0]
    tf2 = [1]
    for i in range(1,N+1):
        range_min = (2*i -1)/ (2*N)
        range_max = (2*i)/ (2*N)
        range_step = (range_max - range_min) / point_by_part
        tmp = range_min
        for j in range(0, point_by_part):
            tf1.append(tmp)
            tmp += range_step

    tf2 = [1 - tf1[i] for i in range(1001)]


    return tf1, tf2

def getProblemTitle():
    return "Unconstrained Problem 6"

def getSearchSpace(problem_size):
    search_space = [[1,(0,1)], [problem_size-1, (-1,1)]]
    return search_space


#FAIRE ATTENTION A PAIRE ET IMPAIRE : il y a un decalage
def f1(x_vector, vector_size):
    global N, epsilon

    decalage = 1
    nb_odd = (vector_size-1) // 2

    x_1 = x_vector[1 - decalage]

    tmp1 = 2 * ((1/ (2 * N)) + epsilon) * math.sin(2 * N * math.pi * x_1)
    tmp2 = 2 / abs(nb_odd)

    sum_y = 0
    product_y = 1
    for odd in range(1 + decalage, vector_size, 2):
        sum_y     += y_function(x_1, x_vector[odd], odd ,vector_size)**2
        product_y *= math.cos(((20 * y_function(x_1, x_vector[odd], odd ,vector_size) * math.pi) / math.sqrt(odd)) + 2)
    tmp3 = 4 * sum_y - 2 * product_y

    return x_1 + max(0, tmp1) + tmp2 * tmp3






def y_function(x_1, x_j, j, n):
    return x_j - math.sin(6 * math.pi * x_1 + ((j * math.pi) / n))



#return number of '0' in a binary string
def f2(x_vector, vector_size):
    global N, epsilon

    decalage = 1
    nb_even = (vector_size-1) // 2 + ((vector_size-1)%2)

    x_1 = x_vector[1 - decalage]

    tmp1 = 2 * ((1/ (2 * N)) + epsilon) * math.sin(2 * N * math.pi * x_1)
    tmp2 = 2 / abs(nb_even)

    sum_y = 0
    product_y = 1
    for even in range(1 + decalage, vector_size, 2):
        sum_y     += y_function(x_1, x_vector[even], even ,vector_size)**2
        product_y *= math.cos(((20 * y_function(x_1, x_vector[even], even ,vector_size) * math.pi) / math.sqrt(even)) + 2)
    tmp3 = 4 * sum_y - 2 * product_y

    return 1 - x_1 + max(0, tmp1) + tmp2 * tmp3
