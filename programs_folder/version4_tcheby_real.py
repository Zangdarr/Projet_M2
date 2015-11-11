#WARNING : be in the program folder to run this program or the relatives links won't work.

import sys
sys.path.insert(0, "../functions_folder/")
import UF1_functions as fct
import operators_functions as op
sys.path.insert(0,"../tools_folder/")
import reals_tchebytchev_tools as tcheby

#-----PARAM-----------------
start_fct    = [fct.uf1_f1, fct.uf1_f2]
operator_fct = [op.DE_Operator, op.polynomial_mutation, op.repair_offspring]
generation_fct = op.genVector
start_fct_len = len(start_fct)

#Shall it maintain an archive and return it in the result ?
manage_archive = False
#stop critera : number of iterations
nb_iterations = 1000
#data parameter : size of the input
vector_size = 30
#size of the neighbourhood, include the current pos
neighboring_size = 21
#no need
nb_flips = 1
#number of new funtions to be generated
N_new_fct = 98 #population size -2
#slow down process parameter
sleeptime = 0
#number max of replacement for each offspring
max_decisions_maj = 2 #nr
#proba to give the neighboring_size. ex : 0 = return always all, 1 = return always neighboring_size
delta_neighbourhood = 0.9
#proba to do the crossover, evaluate for each item in a single vector
CR = 1.0
F = 0.5
#proba to do the mutation, evaluate for each item in a single vector
pm = 1 / vector_size
distrib_index_n = 20


search_space = [[1,(0,1)], [vector_size-1, (-1,1)]]

#####################################################################################################################

#number of functions that will be used for the algorithm
nb_functions = start_fct_len + N_new_fct

result = tcheby.getFrontPareto(start_fct, operator_fct, generation_fct, nb_functions, nb_iterations, neighboring_size, vector_size, nb_flips, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, sleeptime)

#---------------------------------------------------------------------------------------------------------------------
