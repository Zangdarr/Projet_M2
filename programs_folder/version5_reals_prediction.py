#WARNING : be in the program folder to run this program or the relatives links won't work.

import sys
sys.path.insert(0, "../functions_folder/")
import operators_functions as op
sys.path.insert(0,"../tools_folder/")

#-----PARAM-----------------
number_of_functions = 100
operator_fct = [op.DE_Operator, op.polynomial_mutation, op.repair_offspring]
generation_fct = op.genVector
#Shall it maintain an archive and return it in the result ?
manage_archive = False
#size of the neighbourhood, include the current pos
neighboring_size = 21
#slow down process parameter
sleeptime = 0
#number max of replacement for each offspring
max_decisions_maj = 2 #nr
#proba to give the neighboring_size. ex : 0 = return always all, 1 = return always neighboring_size
delta_neighbourhood = 0.9
#proba to do the crossover, evaluate for each item in a single vector
CR = 1.0
F = 0.5
#
distrib_index_n = 20
#size of the neighborhood that will be used for the model training
training_neighborhood_size = 5

#---------------------------------------------------------------------------------------------------------------------

def problemFactory(problem, problem_size):
    global number_of_functions

    if(problem == "UF1"):
        import UF1_functions as fct
        number_of_functions = 100
    elif(problem == "UF2"):
        import UF2_functions as fct
        number_of_functions = 100
    elif(problem == "UF3"):
        import UF3_functions as fct
        number_of_functions = 100
    elif(problem == "UF4"):
        import UF4_functions as fct
        number_of_functions = 100
    elif(problem == "UF5"):
        import UF5_functions as fct
        number_of_functions = 100
    elif(problem == "UF6"):
        import UF6_functions as fct
        number_of_functions = 100
    elif(problem == "UF7"):
        import UF7_functions as fct
        number_of_functions = 100
    elif(problem == "UF8"):
        import UF8_functions as fct
        number_of_functions = 210
    elif(problem == "UF9"):
        import UF9_functions as fct
        number_of_functions = 210
    elif(problem == "UF10"):
        import UF10_functions as fct
        number_of_functions = 210

    return fct.getObjectives(), fct.getFrontPareto, fct.getProblemTitle(), fct.getSearchSpace(problem_size)


def algorithmsFactory(algo_name):
    if(algo_name == "NuSVR-pop"):
        import svm_moea_tools as algo
    elif(algo_name == "NuSVR-popnewest"):
        import svm_moea_pop_newest_tools as algo
    elif(algo_name == "NuSVR-newest"):
        import svm_moea_newest_tools as algo
    elif(algo_name == "NuSVR-fulleval"):
        import svm_moea_full_tools as algo
    elif(algo_name == "NuSVR-freeeval"):
        import svm_moea_tools as algo

    return algo.getFrontParetoWithGraphic, algo.getFrontParetoWithoutGraphic


def runOneTime(algo_name, problem, problem_size, nb_samples, nb_iterations, training_neighborhood_size, strategy, filter_strat):
       global number_of_functions, operator_fct, generation_fct, neighboring_size, max_decisions_maj, delta_neighbourhood, CR, F, distrib_index_n, manage_archive, sleeptime

       start_fct, pareto_front_fct, problem_title, search_space = problemFactory(problem, problem_size)
       N_new_fct = number_of_functions - len(start_fct)
       pm = 1.0 / problem_size

       free_eval = True if "freeeval" in algo_name else False

       getFrontParetoWithGraphic, _ = algorithmsFactory(algo_name)

       getFrontParetoWithGraphic(problem_title, start_fct, operator_fct, generation_fct, pareto_front_fct, number_of_functions, nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, nb_samples, training_neighborhood_size, strategy, filter_strat, free_eval, sleeptime)


def experimentWith(algo_name, problem, file_to_write, problem_size, nb_samples, nb_iterations, training_neighborhood_size, strategy, filter_strat, param_print_every, file_to_writeR2, filenameDIR, filenameSCORE):
       global number_of_functions, operator_fct, generation_fct, neighboring_size, max_decisions_maj, delta_neighbourhood, CR, F, distrib_index_n, manage_archive, sleeptime

       start_fct, pareto_front_fct, problem_title, search_space = problemFactory(problem, problem_size)
       N_new_fct = number_of_functions - len(start_fct)
       pm = 1.0 / problem_size

       free_eval = True if "freeeval" in algo_name else False

       _, getFrontParetoWithoutGraphic = algorithmsFactory(algo_name)

       getFrontParetoWithoutGraphic(start_fct, operator_fct, generation_fct, number_of_functions, nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, nb_samples, training_neighborhood_size, strategy, file_to_write, filter_strat, free_eval, param_print_every, file_to_writeR2, filenameDIR, filenameSCORE, sleeptime)
