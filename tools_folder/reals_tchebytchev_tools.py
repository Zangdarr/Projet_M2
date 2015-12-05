import sys
sys.path.insert(0,"../tools_folder/")
import animated_graph_tools as gph
import generics_tools as gt
import decomposition_tools as dec
sys.path.insert(0, "../functions_folder/")
import math
import space_tools as sp
import numpy as np
import random
import evaluation_tools as eval_to
import archive_tools as arch_to
import initialisation_tools as init_to
#--------------------------------------------------------------------------------------------------------------
archiveOK = False
NO_FILE_TO_WRITE = -1
approx_pareto_front = None

def getResult():
    global approx_pareto_front, archiveOK
    if(archiveOK):
        tmp = approx_pareto_front, arch_to.getArchive()
    else:
        tmp = approx_pareto_front
    return tmp

#--------------------------------------------------------------------------------------------------------------
#  Sampling

def sampling(f, f_neighbors, sampling_param):
    crossover_fct, mutation_fct, repair_fct, best_decisions, F, problem_size, CR, search_space, distrib_index_n, pm = sampling_param
    #select two indice of function in the neighbors + f
    l, k = gt.get_n_elements_of(2, f_neighbors)
    #application of a crossing operator with the current best solution and 2 others from the neighbourhood l & k
    r1, r2, r3 = f, l, k
    mix = crossover_fct(best_decisions[r1],best_decisions[r2],best_decisions[r3], F, problem_size, CR)
    #application of a a bit flip on the newly made solution
    mix_bis = mutation_fct(mix, problem_size, search_space, distrib_index_n, pm)
    #repair step : search space
    mix_ter = repair_fct(mix_bis, search_space)

    return mix_ter





#--------------------------------------------------------------------------------------------------------------
#MAIN ALGORITHMS


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
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, file_to_write]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = gph.runAnimatedGraph(runTcheby,end_function, pareto_front_fct, problem_title ,"f1" ,"f2", sleep=sleeptime)

    #return the approximation of the pareto front and the archive if managed
    return result

def getFrontParetoWithoutGraphic(start_fct, operator_fct, generation_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, file_to_write, sleeptime=10):
    global param, archiveOK
    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = init_to.initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, file_to_write]
    #launch the algorithm
    result = runTcheby()
    #return the approximation of the pareto front and the archive if managed
    return result


def runTcheby():
    global param, nb_evals, approx_pareto_front, archiveOK, nb_evals, NO_FILE_TO_WRITE

    isReals = True
    start_fct, nb_functions                = param[0:2]
    nb_iterations, neighboring_size        = param[2:4]
    init_decisions, problem_size           = param[4:6]
    max_decisions_maj, delta_neighbourhood = param[6:8]
    CR, search_space                       = param[8:10]
    F, distrib_index_n                     = param[10:12]
    pm, operator_fct                       = param[12:14]
    file_to_write                          = param[14]

    best_decisions = init_decisions.copy()
    approx_pareto_front = best_decisions
    #initial best decisions scores
    best_decisions_scores = [eval_to.free_eval(start_fct, best_decisions[i], problem_size) for i in range(nb_functions)]

    nb_evals = 0

    pop_size = nb_functions
    #current optimal scores for both axes
    min_f1 = min(best_decisions_scores[0])
    min_f2 = min(best_decisions_scores[1])
    z_opt_scores = [min_f1, min_f2]

    directions = dec.genRatio_fctbase2(nb_functions)
    crossover_fct, mutation_fct, repair_fct = operator_fct

    sampling_param = [crossover_fct, mutation_fct, repair_fct, best_decisions, F, problem_size, CR, search_space, distrib_index_n, pm]
    writeOK = False
    if(file_to_write != NO_FILE_TO_WRITE):
        writeOK = True
    if(writeOK):
        printObjectives(file_to_write, nb_evals, 0, best_decisions_scores, problem_size)
    #iterations loop
    for itera in range(nb_iterations):
        #functions loop
        for f in range(nb_functions):
            #get all the indice of neighbors of a function in a certain distance of f and include f in
            f_neighbors, current_neighbourhing_size = gt.getNeighborsInclusive(f, neighboring_size, nb_functions, delta_neighbourhood)
            #generate a new valide offspring
            mix_ter = sampling(f, f_neighbors, sampling_param)
            #evaluation of the newly made solution
            mix_scores, nb_evals = eval_to.eval(start_fct, mix_ter, problem_size)
            #MAJ min of f1
            if(mix_scores[0] < min_f1):
                min_f1 = mix_scores[0]
                z_opt_scores[0] = min_f1
            #MAJ min of f2
            if(mix_scores[1] < min_f2):
                min_f2 = mix_scores[1]
                z_opt_scores[1] = min_f2
            #loop on all the neighbors + f
            added_to_S = False
            #count how many best decisions has been changed
            cmpt_best_maj = 0
            #archive not yet
            random.SystemRandom().shuffle(f_neighbors)
            for j in f_neighbors:
                #stop maj best if maj limit reach
                if(cmpt_best_maj >= max_decisions_maj):
                    break
                #if the g_tcheby of the new solution is less distant from the z_optimal solution than the current best solution of the function j
                wj = (directions[0][j],directions[1][j])
                g_mix = eval_to.g_tcheby(wj, mix_scores, z_opt_scores)
                g_best = eval_to.g_tcheby(wj, best_decisions_scores[j], z_opt_scores)
                if( g_mix < g_best):
                    cmpt_best_maj += 1
                    best_decisions[j] = mix_ter
                    best_decisions_scores[j] = mix_scores
                    #if the archive and the solution have not been add already
                    if(archiveOK and not(added_to_S)):
                       arch_to.archivePut(mix_ter, mix_scores)
                       added_to_S = True

        #print("Update", itera, "done.")
        #if manage archive
        if(archiveOK):
           arch_to.maintain_archive()
        #graphic update
        if(writeOK):
            printObjectives(file_to_write, nb_evals, itera+1, best_decisions_scores, problem_size)
            continue
        yield arch_to.getArchiveScore(), best_decisions_scores, itera, nb_evals, min_f1, min_f2, pop_size, isReals

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
