import sys
sys.path.insert(0,"../tools_folder/")
sys.path.insert(0, "../functions_folder/")

import math
import numpy as np
import random, copy

import animated_graph_tools as gph
import archive_tools as arch_to
import decomposition_tools as dec
import evaluation_tools as eval_to
import generics_tools as gt
import initialisation_tools as init_to
import sampling_tools as samp_to
import space_tools as sp
import io_tools as iot
import neighboring_tools as nt

#--------------------------------------------------------------------------------------------------------------
archiveOK = False
NO_FILE_TO_WRITE = "none"
approx_pareto_front = None

def getResult():
    global approx_pareto_front, archiveOK
    if(archiveOK):
        tmp = approx_pareto_front, arch_to.getArchive()
    else:
        tmp = approx_pareto_front
    return tmp

#--------------------------------------------------------------------------------------------------------------
#ACCESSIBLE FUNCTIONS

#algorithm that show on a animated graph the evolution of a population to get a pareto front
param = None
def getFrontParetoWithGraphic(problem_title, start_fct, operator_fct, generation_fct, pareto_front_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, file_to_write, sleeptime=10):
    global param, archiveOK
    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = init_to.initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, "none", -1]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = gph.runAnimatedGraph(runTcheby,end_function, pareto_front_fct, problem_title ,"f1" ,"f2", sleep=sleeptime)

    #return the approximation of the pareto front and the archive if managed
    return result

#algorithm that show on a animated graph the evolution of a population to get a pareto front
def getFrontParetoWithoutGraphic(start_fct, operator_fct, generation_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, file_to_write, param_print_every, sleeptime=10):
    global param, archiveOK
    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = init_to.initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, file_to_write, param_print_every]
    #launch the algorithm
    result = runTcheby()
    #return the approximation of the pareto front and the archive if managed
    return result


def runTcheby():
    global param, approx_pareto_front, archiveOK, NO_FILE_TO_WRITE

    ############################################################################
    # PARAMETER

    isReals = True
    start_fct, nb_functions                = param[0:2]
    nb_iterations, neighboring_size        = param[2:4]
    init_decisions, problem_size           = param[4:6]
    max_decisions_maj, delta_neighbourhood = param[6:8]
    CR, search_space                       = param[8:10]
    F, distrib_index_n                     = param[10:12]
    pm, operator_fct                       = param[12:14]
    file_to_write, param_print_every       = param[14:16]


    nb_objectives = len(start_fct)

    #get separatly offspring operator fct
    crossover_fct, mutation_fct, repair_fct = operator_fct

    best_decisions = copy.deepcopy(init_decisions)

    sampling_param = [crossover_fct, mutation_fct, repair_fct, best_decisions, F, problem_size, CR, search_space, distrib_index_n, pm]

    ############################################################################
    # INITIALISATION

    eval_to.resetEval()

    #get the directions weight for both starting functions
    directions = dec.getDirections(nb_functions, nb_objectives)

    #init the neighboring constant
    nt.initNeighboringTab(nb_functions, neighboring_size, directions, nb_objectives)

    #giving global visibility to the best_decisions to get the result at the end
    approx_pareto_front = best_decisions

    #initial best decisions scores
    best_decisions_scores = [eval_to.free_eval(start_fct, best_decisions[i], problem_size) for i in range(nb_functions)]

    pop_size = nb_functions

    #current optimal scores for both axes
    z_opt_scores = gt.getMinTabOf(best_decisions_scores)

    eval_to.initZstar(z_opt_scores)

    #if the data shall be write in a file
    writeOK = False
    if(file_to_write != NO_FILE_TO_WRITE):
        writeOK = True

    ############################################################################
    # MAIN ALGORITHM

    if(writeOK):
        iot.printObjectives(file_to_write, eval_to.getNbEvals(), 0, best_decisions_scores, problem_size, nb_objectives)

    #IDs tab to allow a random course through the directions in the main loop
    id_directions = [i for i in range(nb_functions)]

    #iterations loop
    for itera in range(nb_iterations):

        #random course through the directions
        random.shuffle(id_directions)

        #functions loop
        for f in id_directions:

            #get all the indice of neighbors of a function in a certain distance of f and include f in
            f_neighbors, current_neighbourhing_size = nt.getNeighborsOf(f, delta_neighbourhood)

            #generate a new valide offspring
            mix_ter = samp_to.sampling(f, f_neighbors, sampling_param)

            #evaluation of the newly made solution
            mix_scores = eval_to.eval(start_fct, mix_ter, problem_size)

            #MAJ of the z_star point
            has_changed = eval_to.min_update_Z_star(mix_scores, nb_objectives)

            #boolean that is True if the offspring has been add to the archive
            added_to_S = False

            #count how many best decisions has been changed by the newly offspring
            cmpt_best_maj = 0

            #random course through the neighbors list
            random.shuffle(f_neighbors)

            #course through the neighbors list
            for j in f_neighbors:

                #stop if already max number of remplacement reach
                if(cmpt_best_maj >= max_decisions_maj):
                    break

                #compute g_tcheby
                #wj = (directions[0][j],directions[1][j])
                wj = [directions[obj][j] for obj in range(0,nb_objectives)]
                g_mix = eval_to.g_tcheby(wj, mix_scores, eval_to.getZstar_with_decal())
                g_best = eval_to.g_tcheby(wj, best_decisions_scores[j], eval_to.getZstar_with_decal())
                #if the g_tcheby of the new solution is less distant from the z_optimal solution than the current best solution of the function j
                if( g_mix < g_best):
                    cmpt_best_maj += 1
                    best_decisions[j] = mix_ter
                    best_decisions_scores[j] = mix_scores
                    #if we manage the archive and the solution have not been add already
                    if(archiveOK and not(added_to_S)):
                       arch_to.archivePut(mix_ter, mix_scores)
                       added_to_S = True
        #print("Update", itera, "done.")

        #if manage archive
        if(archiveOK):
           arch_to.maintain_archive()

        #if write the result in a file
        if(writeOK):
            iot.printObjectives(file_to_write, eval_to.getNbEvals(), itera+1, best_decisions_scores, problem_size, nb_objectives, print_every=param_print_every)
            continue

        #graphic update
        #yield arch_to.getArchiveScore(), best_decisions_scores, itera, eval_to.getNbEvals(), eval_to.getZstar_with_decal(), pop_size, isReals

    return
