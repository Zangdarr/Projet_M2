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
    tf2 = [1 - tf1[i]**2 for i in range(1000)]

    return tf1, tf2

def getProblemTitle():
    return "Unconstrained Problem 4"

def getSearchSpace(problem_size):
    search_space = [[1,(0,1)], [problem_size-1, (-2,2)]]
    return search_space

#FAIRE ATTENTION A PAIRE ET IMPAIRE : il y a un decalage
def f1(x_vector, vector_size):
   #score =  x_1 + factor * sum_y_pow2
   decalage = 1
   nb_odd = (vector_size-1) // 2

   #-----------------------------
   x_1 = x_vector[0]

   factor = 2 / nb_odd

   #-----------------------------

   pi_n = math.pi / vector_size
   cst1 = 6 * math.pi * x_1

   y_tab = [0,0]
   for odd in range(2,vector_size, 2):
       y_part1 = x_vector[odd]

       y_part2 = math.sin(cst1 + (odd+decalage) * pi_n)


       y = y_part1 - y_part2

       y_tab.append(y)
       y_tab.append(0)



   # compute sum on j of yj^2
   #-----------------------------
   sum_h_yj = 0

   for odd in range(2,vector_size, 2):
       h_part_1 = abs(y_tab[odd])

       h_part_2 = 1 + math.exp(2 * h_part_1)

       sum_h_yj += h_part_1 / h_part_2



   return x_1 + factor * sum_h_yj



def f2(x_vector, vector_size):
    x_1 = x_vector[0]
    decalage = 1
    tmp_1 = 1 - x_1**2

    nb_even = (vector_size-1) // 2 + ((vector_size-1)%2)
    factor = 2 / nb_even


    pi_n = math.pi / vector_size
    cst1 = 6 * math.pi * x_1

    y_tab = [0]

    for even in range(1,vector_size, 2):
       y_part1 = x_vector[even]

       y_part2 = math.sin(cst1 + (even+decalage) * pi_n)


       y = y_part1 - y_part2

       y_tab.append(y)
       y_tab.append(0)


    #-----------------------------
    sum_h_yj = 0

    for even in range(1,vector_size, 2):
       h_part_1 = abs(y_tab[even])

       h_part_2 = 1 + math.exp(2 * h_part_1)

       sum_h_yj += h_part_1 / h_part_2


    return tmp_1 + factor * sum_h_yj
