#WARNING : be in the program folder to run this program or the relatives links won't work.

import sys
sys.path.insert(0, "../functions_folder/")
#import UF1_functions as fct
import operators_functions as op
sys.path.insert(0,"../tools_folder/")
import reals_tchebytchev_tools as tcheby

#-----PARAM-----------------
#start_fct    = fct.getObjectives()
number_of_functions = 100
operator_fct = [op.DE_Operator, op.polynomial_mutation, op.repair_offspring]
generation_fct = op.genVector
#start_fct_len = len(start_fct)
#pareto_front_fct = fct.getFrontPareto
#problem_title = fct.getProblemTitle()
#Shall it maintain an archive and return it in the result ?
manage_archive = False
#stop critera : number of iterations
nb_iterations = 100
#data parameter : size of the input
#problem_size = 10
#size of the neighbourhood, include the current pos
neighboring_size = 21
#number of new funtions to be generated
#N_new_fct = number_of_functions - start_fct_len #population size - nb objective function
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
#pm = 1 / problem_size
distrib_index_n = 20


#search_space = fct.getSearchSpace(problem_size)

#####################################################################################################################

#number of functions that will be used for the algorithm
#nb_functions = start_fct_len + N_new_fct

#result = tcheby.getFrontPareto(start_fct, operator_fct, generation_fct, nb_functions, nb_iterations, neighboring_size, problem_size, nb_flips, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, sleeptime)

#---------------------------------------------------------------------------------------------------------------------

def problemFactory(problem, problem_size):
    if(problem == "UF1"):
        import UF1_functions as fct
    elif(problem == "UF2"):
        print("UF2")
        import UF2_functions as fct
    elif(problem == "UF3"):
        import UF3_functions as fct
    elif(problem == "UF4"):
        import UF4_functions as fct
    elif(problem == "UF5"):
        import UF5_functions as fct
    elif(problem == "UF6"):
        import UF6_functions as fct
    elif(problem == "UF7"):
        import UF7_functions as fct
    elif(problem == "UF8"):
        import UF8_functions as fct
    elif(problem == "UF9"):
        import UF9_functions as fct
    elif(problem == "UF10"):
        import UF10_functions as fct

    return fct.getObjectives(), fct.getFrontPareto, fct.getProblemTitle(), fct.getSearchSpace(problem_size)

def runOneTime(problem, problem_size, nb_iterations):
       global number_of_functions, operator_fct, generation_fct, neighboring_size, max_decisions_maj, delta_neighbourhood, CR, F, distrib_index_n, manage_archive, sleeptime

       start_fct, pareto_front_fct, problem_title, search_space = problemFactory(problem, problem_size)
       N_new_fct = number_of_functions - len(start_fct)
       pm = 1 / problem_size

       tcheby.getFrontParetoWithGraphic(problem_title, start_fct, operator_fct, generation_fct, pareto_front_fct, number_of_functions, nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, -1, sleeptime)


def experimentWith(problem, file_to_write, problem_size,  nb_iterations, param_print_every):
       global number_of_functions, operator_fct, generation_fct, neighboring_size, max_decisions_maj, delta_neighbourhood, CR, F, distrib_index_n, manage_archive, sleeptime

       start_fct, pareto_front_fct, problem_title, search_space = problemFactory(problem, problem_size)
       N_new_fct = number_of_functions - len(start_fct)
       pm = 1 / problem_size

       tcheby.getFrontParetoWithoutGraphic(start_fct, operator_fct, generation_fct, number_of_functions, nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, file_to_write, param_print_every, sleeptime)
