import sys
sys.path.insert(0, "../functions_folder/")
sys.path.insert(0, "../prediction_folder/")
sys.path.insert(0, "../tools_folder/")

import copy
import math
import random

import animated_graph_tools as gph
import archive_tools as arch_to
import decomposition_tools as dec
import evaluation_tools as eval_to
import filtring_tools as filt_to
import generics_tools as gt
import initialisation_tools as init_to
import sampling_tools as samp_to
import space_tools as sp
import training_tools as train_to

from sklearn.svm import SVR

#-------------------------------------------------------------------------------
archiveOK = False
NO_FILE_TO_WRITE = -1
approx_pareto_front = None

#-------------------------------------------------------------------------------

def getResult():
    global approx_pareto_front, archiveOK
    if(archiveOK):
        tmp = approx_pareto_front, arch_to.getArchive()
    else:
        tmp = approx_pareto_front
    return tmp

#-------------------------------------------------------------------------------
#ACCESSIBLE FUNCTIONS

#algorithm that show on a animated graph the evolution of a population to get a pareto front
param = None
def getFrontParetoWithGraphic(problem_title, start_fct, operator_fct, generation_fct, pareto_front_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, nb_samples, training_neighborhood_size, strategy, filter_strat, free_eval, sleeptime=10):
    global param, archiveOK
    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = init_to.initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, nb_samples, training_neighborhood_size, strategy, -1, filter_strat, free_eval]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = gph.runAnimatedGraph(runTcheby,end_function, pareto_front_fct, problem_title,"f1" ,"f2", sleep=sleeptime)

    #return the approximation of the pareto front and the archive if managed
    return result



#algorithm that show on a animated graph the evolution of a population to get a pareto front
def getFrontParetoWithoutGraphic(start_fct, operator_fct, generation_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, nb_samples, training_neighborhood_size, strategy, file_to_write, filter_strat, free_eval, sleeptime=10):
    global param, archiveOK

    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = init_to.initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, nb_samples, training_neighborhood_size, strategy, file_to_write, filter_strat, free_eval]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = runTcheby()

    #return the approximation of the pareto front and the archive if managed
    return result



def runTcheby():
    global param, nb_evals, approx_pareto_front, archiveOK, nb_evals, NO_FILE_TO_WRITE

    ############################################################################
    # PARAMETER

    clf = SVR(C=1.0, epsilon=0.2, kernel="rbf")

    isReals = True
    start_fct, nb_functions                = param[0:2]
    nb_iterations, neighboring_size        = param[2:4]
    init_decisions, problem_size           = param[4:6]
    max_decisions_maj, delta_neighbourhood = param[6:8]
    CR, search_space                       = param[8:10]
    F, distrib_index_n                     = param[10:12]
    pm, operator_fct                       = param[12:14]
    nb_samples, training_neighborhood_size = param[14:16]
    strategy, file_to_write                = param[16:18]
    filter_strat, free_eval                = param[18:20]


    #get separatly offspring operator fct
    crossover_fct, mutation_fct, repair_fct = operator_fct

    best_decisions = init_decisions.copy()

    sampling_param = [crossover_fct, mutation_fct, repair_fct, best_decisions, F, problem_size, CR, search_space, distrib_index_n, pm]


    ############################################################################
    # INITIALISATION

    #get the directions weight for both starting functions
    directions = dec.genRatio_fctbase2(nb_functions)

    #giving global visibility to the best_decisions to get the result at the end
    approx_pareto_front = best_decisions

    #initial best decisions scores
    best_decisions_scores = [eval_to.free_eval(start_fct, best_decisions[i], problem_size) for i in range(nb_functions)]

    nb_evals = 0

    pop_size = nb_functions

    #current optimal scores for both axes
    min_f1 = min(best_decisions_scores[0])
    min_f2 = min(best_decisions_scores[1])
    z_opt_scores = [min_f1, min_f2]

    #get the first training part of the item we will learn on
    model_directions = train_to.getDirectionsTrainingMatrix(directions)

    #if the data shall be write in a file
    writeOK = False
    if(file_to_write != NO_FILE_TO_WRITE):
        writeOK = True

    ############################################################################
    # MAIN ALGORITHM

    if(writeOK):
        printObjectives(file_to_write, nb_evals, 0,best_decisions_scores, problem_size)

    #iterations loop
    for itera in range(nb_iterations):
        #Update model
        training_input, training_output = train_to.getTrainingSet(model_directions, best_decisions, best_decisions_scores ,z_opt_scores, strategy, nb_functions, training_neighborhood_size)
        clf.fit(training_input, training_output)

        #functions loop
        for f in range(nb_functions):

            #get all the indice of neighbors of a function in a certain distance of f and include f in
            f_neighbors, current_neighbourhing_size = gt.getNeighborsInclusive(f, neighboring_size, nb_functions, delta_neighbourhood)

            #get a list of offspring from the neighbors
            list_offspring = samp_to.extended_sampling(f, f_neighbors, sampling_param, nb_samples)

            #apply a filter on the offspring list and select the best one
            filter_param = [clf, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_opt_scores, best_decisions_scores]
            best_candidate = filt_to.model_based_filtring(filter_strat, free_eval, filter_param)

            #evaluation of the newly made solution
            mix_scores, nb_evals = eval_to.eval(start_fct, best_candidate, problem_size)

            #MAJ of the z_star point
            if(mix_scores[0] < min_f1):
                min_f1 = mix_scores[0]
                z_opt_scores[0] = min_f1
            if(mix_scores[1] < min_f2):
                min_f2 = mix_scores[1]
                z_opt_scores[1] = min_f2

            #boolean that is True if the offspring has been add to the archive
            added_to_S = False

            #count how many best decisions has been changed by the newly offspring
            cmpt_best_maj = 0

            #random course through the neighbors list
            random.SystemRandom().shuffle(f_neighbors)

            #course through the neighbors list
            for j in f_neighbors:

                #stop if already max number of remplacement reach
                if(cmpt_best_maj >= max_decisions_maj):
                    break

                #compute g_tcheby
                wj = (directions[0][j],directions[1][j])
                g_mix = eval_to.g_tcheby(wj, mix_scores, z_opt_scores)
                g_best = eval_to.g_tcheby(wj, best_decisions_scores[j], z_opt_scores)

                #if the g_tcheby of the new solution is less distant from the z_optimal solution than the current best solution of the function j
                if(g_mix < g_best):
                    cmpt_best_maj += 1
                    best_decisions[j] = best_candidate
                    best_decisions_scores[j] = mix_scores

                    #if we manage the archive and the solution have not been add already
                    if(archiveOK and not(added_to_S)):
                       arch_to.archivePut(best_candidate, mix_scores)
                       added_to_S = True
        #print("Update", itera, "done.")

        #if manage archive
        if(archiveOK):
           arch_to.maintain_archive()

        #if write the result in a file
        if(writeOK):
            printObjectives(file_to_write, nb_evals, itera+1, best_decisions_scores, problem_size)
            continue

        #graphic update
        yield arch_to.getArchiveScore(), best_decisions_scores, itera+1, nb_evals, min_f1, min_f2, pop_size, isReals

    return 1


def printObjectives(file_to_write, eval_number,iteration_number,  objectives_table, problem_size):
    if(iteration_number % problem_size == 0):
        tab = [''," ", '', " ", '', " ", '', "\n"]
        for objectives in objectives_table:
            tab[0] = str(iteration_number)
            tab[2] = str(eval_number)
            tab[4] = str(objectives[0])
            tab[6] = str(objectives[1])


            file_to_write.write(''.join(tab))
            #print(iteration_number, eval_number, objectives[0], objectives[1])
