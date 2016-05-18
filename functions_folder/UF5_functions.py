import math

########################################################################
# Parameters from CEC'09
########################################################################
N = 10
epsilon = 0.1

########################################################################
# Objective functions
########################################################################
def getObjectives():
    return [f1, f2]


def getFrontPareto():
    global N

    tf1 = []
    tf2 = []

    for i in range((2 * N) + 1):
        tf1.append(i / float(2 * N))
        tf2.append(1 - tf1[i])

    return tf1, tf2

def getProblemTitle():
    return "Unconstrained Problem 5"


def getSearchSpace(problem_size):
    search_space = [[1,(0,1)], [problem_size-1, (-1,1)]]
    return search_space

#FAIRE ATTENTION A PAIRE ET IMPAIRE : il y a un decalage
def f1(x_vector, vector_size):
    global N, epsilon

    decalage = 1
    nb_odd = (vector_size-1) // 2

    x_1 = x_vector[1 - decalage]
    tmp1 = ((1.0 / (2 * N)) + epsilon) * abs(math.sin(2 * N * math.pi * x_1))
    tmp2 = 2.0 / abs(nb_odd)

    sum_h = 0
    for odd in range(1 + decalage, vector_size, 2):
        sum_h += h_function(y_function(x_1, x_vector[odd], odd ,vector_size))


    return x_1 + tmp1 + tmp2 * sum_h

def y_function(x_1, x_j, j, n):
    return x_j - math.sin(6 * math.pi * x_1 + ((j * math.pi) / float(n)))

def h_function(t):
    return 2 * t**2 - math.cos(4 * math.pi * t) + 1


#return number of '0' in a binary string
def f2(x_vector, vector_size):
    global N, epsilon

    decalage = 1
    nb_even = (vector_size-1) // 2 + ((vector_size-1)%2)

    x_1 = x_vector[1 - decalage]
    tmp1 = ((1.0 / (2 * N)) + epsilon) * abs(math.sin(2 * N * math.pi * x_1))
    tmp2 = 2.0 / abs(nb_even)

    sum_h = 0
    for even in range(0+decalage, vector_size, 2):
        sum_h += h_function(y_function(x_1, x_vector[even], even ,vector_size))

    return 1 - x_1 + tmp1 + tmp2 * sum_h
