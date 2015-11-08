import sys
sys.path.insert(0,"../tools_folder/")
import animated_graph_tools as gph
import generics_tools as gt
import decomposition_tools as dec
sys.path.insert(0, "../functions_folder/")
import bitstring_functions as fct
import math
import space_tools as sp

#--------------------------------------------------------------------------------------------------------------
archive = []
def archivePut(solution, score):
    return "not yet"
    """
    global archive
    archive.append((solution, score))
    """
def archiveGet():
    global archive
    return archive
#Randomly initialise the best solution for each functions generated
def initRandom(decision_space, nb_functions, taille):
    tab = []
    for i in range(nb_functions):#taille de la pop
        tmp_bs = fct.genBS(taille)
        decision_space.append(tmp_bs)
        tab.append(tmp_bs)
    return tab

#evaluate the distance of a solution from the z-optimal solution
def g_tcheby(dir, score, opt_scores):
    return max(dir[0]*abs(score[0]-opt_scores[0]),dir[1]*abs(score[1]-opt_scores[1]))

#evaluation of an offspring with the 2 base functions
nb_evals = 0
def eval(start_fct, bitstring):
    global nb_evals
    nb_evals += 1
    bs_scores = [start_fct[f](bitstring) for f in range(len(start_fct))]
    return bs_scores

#--------------------------------------------------------------------------------------------------------------

#algorithm that show on a animated graph the evolution of a population to get a pareto front
param = None
def getFrontPareto(start_fct, nb_functions, decision_space, objective_space,
               nb_iterations, neighboring_size, bitstring_size, nb_flips,sleeptime=10):
    global param
    #random initialisation
    init_decisions = initRandom(decision_space, nb_functions, bitstring_size)
    #get objective space representation of the solution
    objective_space = sp.getObjectiveSpace(start_fct, decision_space)
    #algorithm parameters
    param = [objective_space, decision_space, start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, bitstring_size, nb_flips]
    #launch the graphic view and the algorithm
    result = gph.runAnimatedGraph(runTcheby,"Front pareto Tcheby Evolution","f1 - count 1" ,"f2 - count 0", sleep=sleeptime)

    return result


def runTcheby():
    global param, nb_evals

    objective_space, decision_space          = param[0:2]
    start_fct, nb_functions               = param[2:4]
    nb_iterations, neighboring_size          = param[4:6]
    init_decisions, bitstring_size, nb_flips = param[6:]
    best_decisions = init_decisions.copy()

    #start_fct + new_fct
    #current optimal scores for both axes
    max_f1 = max(objective_space[0])
    max_f2 = max(objective_space[1])
    z_opt_scores = [max_f1, max_f2]
    #initial best decisions scores
    best_decisions_scores = [eval(start_fct, best_decisions[i]) for i in range(nb_functions)]

    directions = dec.genRatio_fctbase2(nb_functions-2)
    #iterations loop
    for itera in range(nb_iterations):
        #functions loop
        for f in range(nb_functions):
            #get all the indice of neighbors of a function in a certain distance of f and include f in
            f_neighbors = gt.getNeighborsInclusive(f, neighboring_size, nb_functions)
            #select two indice of function in the neighbors + f
            l, k = gt.get_n_elements_of(2, f_neighbors)
            #application of a crossing operator between the current best solution of l and k
            mix = fct.mixOperator(best_decisions[l],best_decisions[k], p=0.1)
            #application a a bit flip on the newly made solution
            mix_bis = fct.bitflip(mix, flip=nb_flips)
            #evaluation of the newly made solution
            mix_scores = eval(start_fct, mix_bis)
            #MAJ max of f1
            if(mix_scores[0] > max_f1):
                max_f1 = mix_scores[0]
                z_opt_scores[0] = max_f1
            #MAJ max of f2
            if(mix_scores[1] > max_f2):
                max_f2 = mix_scores[1]
                z_opt_scores[1] = max_f2
            #loop on all the neighbors + f
            added_to_S = False
            #archive not yet
            archivePut(mix_bis, mix_scores)
            for j in f_neighbors:
                #if the g_tcheby of the new solution is less distant from the z_optimal solution than the current best solution of the function j
                wj = (directions[0][j]/directions[2][j],directions[1][j]/directions[2][j])
                if(g_tcheby(wj, mix_scores, z_opt_scores) < g_tcheby(wj, best_decisions_scores[j], z_opt_scores)):
                    best_decisions[j] = mix_bis
                    best_decisions_scores[j] = mix_scores
                    if(not(added_to_S)):
                       objective_space[0].append(mix_scores[0])
                       objective_space[1].append(mix_scores[1])
                       decision_space.append(mix_bis)
                       added_to_OS = True


        print("Update", itera, "done.")
        #graphic update
        yield objective_space, best_decisions_scores, itera, nb_evals, max_f1, max_f2

    return objective_space, best_decisions_scores, itera, nb_evals,  max_f1, max_f2
