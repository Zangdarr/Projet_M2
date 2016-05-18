import math

########################################################################
# Parameters from CEC'09
########################################################################

epsilon = 0.1

########################################################################
# Objective functions
########################################################################
def getObjectives():
    return [f1, f2, f3]

def getFrontPareto():
    tf1 = []
    tf2 = []
    tf3 = []

    f3_range_min = 0.0
    f3_range_max = 1.0
    part_size = 500
    f3_step_size = (f3_range_max - f3_range_min) / float(part_size)

    f3 = -1 * f3_step_size
    for if3 in range(0, part_size // 2):
        f3 += f3_step_size
        f1_step_size = ((1/4.0) * (1 - f3)) / float(part_size)
        f1 = -1 * f1_step_size
        for if1 in range(0, part_size // 2):
            f1 += f1_step_size
            f2 = 1 - f1 - f3

            tf1.append(f1)
            tf2.append(f2)
            tf3.append(f3)


    f3 = -1 * f3_step_size
    for if3 in range(0, part_size // 2):
        f3 += f3_step_size
        f1_step_size = (1.0 - (3/4.0) * (1 - f3)) / float(part_size)
        f1 = -1 * f1_step_size
        for if1 in range(0, part_size // 2):
            f1 += f1_step_size
            f2 = 1 - f1 - f3

            tf1.append(f1)
            tf2.append(f2)
            tf3.append(f3)



    return tf1, tf2, tf3



def getProblemTitle():
    return "Unconstrained Problem 9"

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


    sum_j_pow2 = 0
    for j in range(3, vector_size, 3):
        sum_j_pow2 += (x_vector[j] - 2 * x_2 * math.sin(2 * math.pi * x_1 + ((j * math.pi)/ vector_size)))**2

    tmp11 = 1.0 + epsilon
    tmp12 = 1 - 4 * (2 * x_1 -1)**2
    final1 = max(0, tmp11 * tmp12) + 2 * x_1
    final2 = 2.0 / abs(j1)


    return 0.5 * final1 * x_2 + final2 * sum_j_pow2


def f2(x_vector, vector_size):
    global N, epsilon, j2

    if(j2 == -1):
        initJ(vector_size)

    x_1 = x_vector[0]
    x_2 = x_vector[1]


    sum_j_pow2 = 0
    for j in range(4, vector_size, 3):
        sum_j_pow2 += (x_vector[j] - 2 * x_2 * math.sin(2 * math.pi * x_1 + ((j * math.pi)/ vector_size)))**2

    tmp11 = 1.0 + epsilon
    tmp12 = 1.0 - 4.0 * (2.0 * x_1 - 1.0)**2
    final1 = max(0, tmp11 * tmp12) - 2 * x_1 + 2
    final2 = 2.0 / abs(j2)


    return 0.5 * final1 * x_2 + final2 * sum_j_pow2



def f3(x_vector, vector_size):
    global N, epsilon, j3

    if(j3 == -1):
        initJ(vector_size)

    x_1 = x_vector[0]
    x_2 = x_vector[1]


    sum_j_pow2 = 0.0
    for j in range(2, vector_size, 3):
        sum_j_pow2 += (x_vector[j] - 2 * x_2 * math.sin(2 * math.pi * x_1 + ((j * math.pi)/ vector_size)))**2

    final2 = 2.0 / abs(j3)


    return 1.0 - x_2 + final2 * sum_j_pow2
