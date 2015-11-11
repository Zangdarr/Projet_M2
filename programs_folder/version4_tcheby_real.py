#WARNING : be in the program folder to run this program or the relatives links won't work.

import sys
sys.path.insert(0, "../functions_folder/")
import UF_functions as fct
sys.path.insert(0,"../tools_folder/")
import reals_tchebytchev_tools as tcheby

#-----PARAM-----------------
start_fct = [fct.uf1_f1, fct.uf1_f2]
start_fct_len = len(start_fct)

nb_iterations = 1000
vector_size = 30
neighboring_size = 21
nb_flips = 1
N_new_fct = 98 #population size -2
sleeptime = 0
max_decisions_maj = 2 #nr
delta_neighbourhood = 0.1
CR = 1.0
F = 0.5
pm = 1 / vector_size
distrib_index_n = 20


search_space = [[1,(0,1)], [vector_size-1, (-1,1)]]

#####################################################################################################################

decision_space = []

objective_space = []

#number of functions that will be used for the algorithm
nb_functions = start_fct_len + N_new_fct

result = tcheby.getFrontPareto(start_fct, nb_functions, decision_space, objective_space, nb_iterations, neighboring_size, vector_size, nb_flips, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, sleeptime)

#---------------------------------------------------------------------------------------------------------------------
