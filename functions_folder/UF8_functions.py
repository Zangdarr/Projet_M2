import math


########################################################################
# Objective functions
########################################################################
def getObjectives():
    return [f1, f2, f3]

def getFrontPareto():
    tf1 = []
    tf2 = []
    tf3 = []

    nb_steps = 100
    range_min = 0.0
    range_max = 1.0
    step_size = (range_max - range_min) / float(nb_steps)

    f1 = -1 * step_size
    f2 = -1 * step_size
    f3 = -1 * step_size

    epsilon = 0.00000000001

    cmpt = 0

    for if1 in range(0,nb_steps):
        f1 += step_size
        f2 = -1 * step_size
        for if2 in range(0,nb_steps):
            f2 += step_size
            f3 = -1 * step_size
            for if3 in range(0,nb_steps):
                f3 += step_size
                tmp = f1**2 + f2**2 + f3**3
                if( 1.0 - epsilon <=  tmp  <= 1.0 + epsilon):
                    tf1.append(f1)
                    tf2.append(f2)
                    tf3.append(f3)

    return tf1, tf2, tf3



def getProblemTitle():
    return "Unconstrained Problem 8"

def getSearchSpace(problem_size):
    search_space = [[2,(0,1)], [problem_size-2, (-2,2)]]
    return search_space


j1 = -1
j2 = -1
j3 = -1

def initJ(vector_size):
    global j1, j2, j3
    j1 = 0
    j2 = 0
    j3 = 0

    for j in range(3, vector_size):
        if(j % 3 == 0):
            j3 += 1
        elif(j %  3 == 2):
            j2 += 1
        else:
            j1 += 1

def f1(x_vector, vector_size):
    global N, epsilon, j1

    if(j1 == -1):
        initJ(vector_size)

    x_1 = x_vector[0]
    x_2 = x_vector[1]

    tmp1 = math.cos(0.5 * x_1 * math.pi)
    tmp2 = math.cos(0.5 * x_2 * math.pi)
    tmp3 = 2.0 / abs(j1)

    sum_j = 0
    for j in range(3, vector_size, 3):
        sum_j += (x_vector[j] - 2 * x_2 * math.sin(2 * math.pi * x_1 + ((j * math.pi)/ float(vector_size))))**2


    return tmp1 * tmp2 + tmp3 * sum_j

def f2(x_vector, vector_size):
    global N, epsilon, j2

    if(j2 == -1):
        initJ(vector_size)

    x_1 = x_vector[0]
    x_2 = x_vector[1]

    tmp1 = math.cos(0.5 * x_1 * math.pi)
    tmp2 = math.sin(0.5 * x_2 * math.pi)
    tmp3 = 2.0 / abs(j2)

    sum_j = 0
    for j in range(4, vector_size, 3):
        sum_j += (x_vector[j] - 2 * x_2 * math.sin(2 * math.pi * x_1 + ((j * math.pi)/ float(vector_size))))**2


    return tmp1 * tmp2 + tmp3 * sum_j




def f3(x_vector, vector_size):
    global N, epsilon, j3

    if(j3 == -1):
        initJ(vector_size)

    x_1 = x_vector[0]
    x_2 = x_vector[1]

    tmp1 = math.sin(0.5 * x_1 * math.pi)
    tmp2 = 2.0 / abs(j3)

    sum_j = 0
    for j in range(2, vector_size, 3):
        sum_j += (x_vector[j] - 2 * x_2 * math.sin(2 * math.pi * x_1 + ((j * math.pi)/ float(vector_size))))**2


    return tmp1 + tmp2 * sum_j
