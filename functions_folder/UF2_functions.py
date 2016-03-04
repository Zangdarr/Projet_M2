import random
import math
import numpy

########################################################################
# Objective functions
########################################################################

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
    return "Unconstrained Problem 2"


def getSearchSpace(problem_size):
    search_space = [[1,(0,1)], [problem_size-1, (-1,1)]]
    return search_space

#FAIRE ATTENTION A PAIRE ET IMPAIRE : il y a un decalage
def f1(x_vector, vector_size):
   #score =  x_1 + factor * sum_y_pow2
   decalage = 1
   nb_odd = (vector_size-1) // 2
   #-----------------------------
   x_1 = x_vector[0]

   factor = 2 / nb_odd

   sum_y_pow2 = 0
   #-----------------------------
   pi_n = math.pi / vector_size

   cst1 = 24 * math.pi * x_1
   cst2 = 6 * math.pi * x_1
   cst3 = 0.6 * x_1
   for odd in range(2,vector_size, 2):
       y_part1 = x_vector[odd]

       y_tmp  = 4 * (odd+decalage) * pi_n
       y_part2 = 0.3 * (x_1**2) *  math.cos(cst1 + y_tmp)

       y_tmp  = (odd+decalage) * pi_n
       y_part3 = math.cos(cst2 + y_tmp)

       y = y_part1 - (y_part2 + cst3) * y_part3

       sum_y_pow2 += y**2

   return x_1 + factor * sum_y_pow2



def f2(x_vector, vector_size):
    x_1 = x_vector[0]
    decalage = 1
    tmp_1 = 1 - math.sqrt(x_1)

    nb_even = (vector_size-1) // 2 + ((vector_size-1)%2)
    tmp_2 = 2 / nb_even

    sum_y_pow2 = 0
    cst1 = 24 * math.pi * x_1
    cst2 = 6 * math.pi * x_1
    cst3 = 0.6 * x_1

    pi_n = math.pi / vector_size
    for even in range(1,vector_size, 2):
        y_part1 = x_vector[even]

        y_tmp  = 4 * (even+decalage) * pi_n
        y_part2 = 0.3 * (x_1**2) * math.cos(y_tmp + cst1)

        y_tmp  = (even+decalage) * pi_n
        y_part3 = math.sin(cst2 + y_tmp)

        y = y_part1 - (y_part2 + cst3) * y_part3

        sum_y_pow2 += y**2

    return tmp_1 + tmp_2 * sum_y_pow2
