#WARNING : be in the program folder to run this program or the relatives links won't work.

import sys
sys.path.insert(0, "../functions_folder/")
import bitstring_functions as fct
sys.path.insert(0,"../tools_folder/")
import tchebytchev_tools as tcheby

#-----PARAM-----------------
start_fct = [fct.f1, fct.f2]
start_fct_len = len(start_fct)

nb_iterations = 1000
bitstring_size = 100
neighboring_size = 3
nb_flips = 1
N_new_fct = 20
sleeptime = 0

#####################################################################################################################

decision_space = []

objective_space = []

#number of functions that will be used for the algorithm
nb_functions = start_fct_len + N_new_fct

result = tcheby.getFrontPareto(start_fct, nb_functions, decision_space, objective_space, nb_iterations, neighboring_size, bitstring_size, nb_flips, sleeptime)

#---------------------------------------------------------------------------------------------------------------------
