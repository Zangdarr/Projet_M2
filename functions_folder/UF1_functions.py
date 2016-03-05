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
    tf2 = [1 - math.sqrt(tf1[i]) for i in range(1000)]

    return tf1, tf2

def getProblemTitle():
    return "Unconstrained Problem 1"


def getSearchSpace(problem_size):
    search_space = [[1,(0,1)], [problem_size-1, (-1,1)]]
    return search_space

#FAIRE ATTENTION A PAIRE ET IMPAIRE : il y a un decalage
def f1(x_vector, vector_size):
   decalage = 1
   tmp_1 = x_vector[0]

   nb_odd = (vector_size-1) // 2
   tmp_2 = 2 / nb_odd

   tmp_3 = 0
   sin_tmp_1 = 6 * math.pi * tmp_1
   pi_n = math.pi / vector_size

   for odd in range(2,vector_size, 2):
       sin_tmp_2 = odd+decalage * pi_n
       tmp_3 += x_vector[odd] - math.sin(sin_tmp_1 + sin_tmp_2)

   return tmp_1 + tmp_2 * math.pow(tmp_3,2)


#return number of '0' in a binary string
def f2(x_vector, vector_size):
    x_1 = x_vector[0]
    decalage = 1
    tmp_1 = 1 - math.sqrt(x_1)

    nb_even = (vector_size-1) // 2 + ((vector_size-1)%2)
    tmp_2 = 2 / nb_even

    tmp_3 = 0
    sin_tmp_1 = 6 * math.pi * x_1
    pi_n = math.pi / vector_size
    for even in range(1,vector_size, 2):
        sin_tmp_2 = (even+decalage) * pi_n
        tmp_3 += x_vector[even] - math.sin(sin_tmp_1 + sin_tmp_2)

    return tmp_1 + tmp_2 * math.pow(tmp_3,2)
