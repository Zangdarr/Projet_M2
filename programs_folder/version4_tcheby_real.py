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
vector_size = 4
neighboring_size = 3
nb_flips = 1
N_new_fct = 20
sleeptime = 0
max_decisions_maj = 3
delta_neighbourhood = 0.5
CR = 0.9
F = 1
pm = 0.9
distrib_index_n = 10


search_space = [[1,(0,1)], [vector_size-1, (-1,1)]]

#####################################################################################################################

decision_space = []

objective_space = []

#number of functions that will be used for the algorithm
nb_functions = start_fct_len + N_new_fct

result = tcheby.getFrontPareto(start_fct, nb_functions, decision_space, objective_space, nb_iterations, neighboring_size, vector_size, nb_flips, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, sleeptime)

#---------------------------------------------------------------------------------------------------------------------
