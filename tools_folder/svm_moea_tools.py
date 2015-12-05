import sys
sys.path.insert(0,"../prediction_folder/")
import training_tools as train_to
sys.path.insert(0,"../tools_folder/")
import animated_graph_tools as gph
import generics_tools as gt
import decomposition_tools as dec
sys.path.insert(0, "../functions_folder/")
import math
import space_tools as sp
import numpy as np
import random
import copy
import evaluation_tools as eval_to

from sklearn.svm import SVR

#--------------------------------------------------------------------------------------------------------------
#ARCHIVE
archive_sol = []
archive_score = [[],[]]
archive_size = 0
archiveOK = False
NO_FILE_TO_WRITE = -1

def archivePut(solution, score):
    global archive_sol, archive_score, archive_size
    archive_sol.append(solution)
    archive_score[0].append(score[0])
    archive_score[1].append(score[1])
    archive_size += 1

def maintain_archive():
    global archive_sol, archive_score, archive_size
    archive_sol, archive_score, archive_size = maintain_population(archive_sol, archive_score, archive_size)

#--------------------------------------------------------------------------------------------------------------
approx_pareto_front = None

def getResult():
    global archive_sol, approx_pareto_front, archiveOK
    if(archiveOK):
        tmp = approx_pareto_front, archive_sol
    else:
        tmp = approx_pareto_front
    return tmp
#--------------------------------------------------------------------------------------------------------------
#INITIALISATION

#Randomly initialise the best solution for each functions generated
def initRandom(generation_fct, nb_functions, problem_size, search_space):
    tab = []
    for i in range(nb_functions):
        tmp = generation_fct(problem_size, search_space)
        tab.append(tmp)
    return tab


def maintain_population(decision_space, objective_space, pop_size):
    OS_0 = objective_space[0]
    OS_1 = objective_space[1]

    defenders_DS = []
    defenders_OS_0 = []
    defenders_OS_1 = []

    defenders_DS.append(decision_space[0])
    defenders_OS_0.append(OS_0[0])
    defenders_OS_1.append(OS_1[0])

    nb_defenders = 1
    for challenger in range(1, pop_size):
        challenger_isDominated = False
        defenders_tokill = []
        for defender in range(nb_defenders):
              fight0_result = OS_0[challenger] - defenders_OS_0[defender]
              fight1_result = OS_1[challenger] - defenders_OS_1[defender]
              if(fight0_result >= 0 and fight1_result >= 0): #challenger is dominated by the defender#MIN
                 challenger_isDominated = True
                 break
              elif(fight0_result < 0 and fight1_result < 0): #challenger is dominating the defender #MIN
                 defenders_tokill.append(defender)
              else: #same score
                 pass
        #killing the dominated ones
        nb_defenders_to_kill = len(defenders_tokill)
        for last in range(nb_defenders_to_kill-1, -1, -1 ):
                del defenders_DS[defenders_tokill[last]]
                del defenders_OS_0[defenders_tokill[last]]
                del defenders_OS_1[defenders_tokill[last]]
        nb_defenders -= nb_defenders_to_kill
        #add challenger if not dominated
        if(not(challenger_isDominated)):
            nb_defenders += 1
            defenders_DS.append(decision_space[challenger])
            defenders_OS_0.append(OS_0[challenger])
            defenders_OS_1.append(OS_1[challenger])

    return defenders_DS, [defenders_OS_0, defenders_OS_1], nb_defenders


#--------------------------------------------------------------------------------------------------------------
#EXTENDED SAMPLING

def extended_sampling(f,f_neighbors, sampling_param, nb_samples):
    l = []
    for i in range(nb_samples):
        l.append(sampling(f,f_neighbors, sampling_param))
    return l


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
# MODEL-BASED-FILTRING


def model_based_filtring(model, f_neighbors, list_offspring, model_directions):
    id_offspring = -1
    index_best = -1
    score_best = 0
    for offspring in list_offspring:
        id_offspring += 1
        average_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)

        count = 0
        for data in f_input_data:
            tmp = model.predict(data)
            average_score += tmp
            count +=1

        average_score /= count
        if(index_best == -1):
            index_best = id_offspring
            score_best = average_score
        elif(average_score < score_best):
            index_best = id_offspring
            score_best = average_score
        else :
            pass

    return list_offspring[index_best]



def getInputData(f_neighbors, model_directions, offspring):
    l= []
    id_l = -1
    for i in f_neighbors:
        id_l += 1
        l.append([])

        l[id_l].extend(model_directions[i].tolist()[0])

        l[id_l].extend(offspring)

    return np.matrix(l)



#--------------------------------------------------------------------------------------------------------------
#MAIN ALGORITHMS

#algorithm that show on a animated graph the evolution of a population to get a pareto front
param = None
def getFrontParetoWithGraphic(problem_title, start_fct, operator_fct, generation_fct, pareto_front_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, nb_samples, training_neighborhood_size, strategy, sleeptime=10):
    global param, archiveOK
    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, nb_samples, training_neighborhood_size, strategy, -1]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = gph.runAnimatedGraph(runTcheby,end_function, pareto_front_fct, problem_title,"f1" ,"f2", sleep=sleeptime)

    #return the approximation of the pareto front and the archive if managed
    return result



#algorithm that show on a animated graph the evolution of a population to get a pareto front
def getFrontParetoWithoutGraphic(start_fct, operator_fct, generation_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, nb_samples, training_neighborhood_size, strategy, file_to_write, sleeptime=10):
    global param, archiveOK

    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, nb_samples, training_neighborhood_size, strategy, file_to_write]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = runTcheby()

    #return the approximation of the pareto front and the archive if managed
    return result


def runTcheby():
    global param, nb_evals, archive_score, approx_pareto_front, archiveOK, nb_evals, NO_FILE_TO_WRITE

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

    #initial best g_tcheby scores
    best_g_tcheby = [eval_to.g_tcheby((directions[0][i], directions[1][i]), best_decisions_scores[i], z_opt_scores) for i in range(nb_functions)]


    #get the first training part of the item we will learn on
    model_directions = train_to.getDirectionsTrainingMatrix(directions)


    ############################################################################
    # MAIN ALGORITHM
    writeOK = False
    if(file_to_write != NO_FILE_TO_WRITE):
        writeOK = True
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

            list_offspring = extended_sampling(f, f_neighbors, sampling_param, nb_samples)

            best_candidate = model_based_filtring(clf, f_neighbors, list_offspring, model_directions)

            #evaluation of the newly made solution
            mix_scores, nb_evals = eval_to.eval(start_fct, best_candidate, problem_size)
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
                #if(g_mix < best_g_tcheby[j]):
                if(g_mix < g_best):
                    cmpt_best_maj += 1
                    best_decisions[j] = best_candidate
                    best_decisions_scores[j] = mix_scores
                    best_g_tcheby[j] = g_mix
                    #if we manga the archive and the solution have not been add already
                    if(archiveOK and not(added_to_S)):
                       archivePut(best_candidate, mix_scores)
                       added_to_S = True

        #print("Update", itera, "done.")
        #if manage archive
        if(archiveOK):
           maintain_archive()
        #graphic update
        if(writeOK):
            printObjectives(file_to_write, nb_evals, itera+1, best_decisions_scores, problem_size)
            continue

        yield archive_score, best_decisions_scores, itera+1, nb_evals, min_f1, min_f2, pop_size, isReals

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
