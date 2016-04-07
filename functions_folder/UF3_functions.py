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
    return "Unconstrained Problem 3"

def getSearchSpace(problem_size):
    search_space = [[problem_size,(0,1)]]
    return search_space

#FAIRE ATTENTION A PAIRE ET IMPAIRE : il y a un decalage
def f1(x_vector, vector_size):
   #score =  x_1 + factor * sum_y_pow2
   decalage = 1
   nb_odd = (vector_size-1) // 2

   #-----------------------------
   x_1 = x_vector[0]

   factor = 2.0 / nb_odd


   #-----------------------------
   # compute sum on j of yj^2
   sum_y_pow2 = 0

   y_tab = [0,0]
   for odd in range(2,vector_size, 2):
       y_part1 = x_vector[odd]

       y_tmp_1 = (3 * (odd+decalage - 2)) / float(vector_size - 2)
       y_tmp  = 0.5 * (1.0 + y_tmp_1)

       y_part2 = x_1**(y_tmp)


       y = y_part1 - y_part2

       y_tab.append(y)
       y_tab.append(0)
       sum_y_pow2 += y**2

   #-----------------------------
   product_cos = 1

   for odd in range(2,vector_size, 2):
       cos_part_1 = 20 * y_tab[odd] * math.pi

       cos_part_2 = math.sqrt(odd + decalage)



       product_cos *= math.cos(float(cos_part_1) / cos_part_2)



   return x_1 + factor * (4 * sum_y_pow2 - 2 * product_cos + 2)



def f2(x_vector, vector_size):
    x_1 = x_vector[0]
    decalage = 1
    tmp_1 = 1 - math.sqrt(x_1)

    nb_even = (vector_size-1) // 2 + ((vector_size-1)%2)
    factor = 2.0 / nb_even

    sum_y_pow2 = 0
    y_tab = [0]

    for even in range(1,vector_size, 2):
       y_part1 = x_vector[even]

       y_tmp_1 = (3 * (even+decalage - 2)) / float(vector_size - 2)
       y_tmp  = 0.5 * (1.0 + y_tmp_1)

       y_part2 = x_1**(y_tmp)


       y = y_part1 - y_part2
       y_tab.append(y)
       y_tab.append(0)
       sum_y_pow2 += y**2


    #-----------------------------
    product_cos = 1

    for even in range(1,vector_size, 2):
        cos_part_1 = 20 * y_tab[even] * math.pi
        cos_part_2 = math.sqrt(even+decalage)

        product_cos *= math.cos(float(cos_part_1) / cos_part_2)

    return tmp_1 + factor * (4 * sum_y_pow2 - 2 * product_cos + 2)
