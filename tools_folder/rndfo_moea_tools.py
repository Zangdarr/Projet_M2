import sys
sys.path.insert(0, "../functions_folder/")
sys.path.insert(0, "../prediction_folder/")
sys.path.insert(0, "../tools_folder/")

import copy
import math
import random
import numpy

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
import io_tools as iot
import model_quality_tools as qual_tools
import neighboring_tools as nt


from sklearn.ensemble import RandomForestRegressor
from sklearn import grid_search
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score

#-------------------------------------------------------------------------------
archiveOK = False
NO_FILE_TO_WRITE = "none"
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
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, nb_samples, training_neighborhood_size, strategy, "none", filter_strat, free_eval, -1, "none", "none", "none"]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = gph.runAnimatedGraph(runTcheby,end_function, pareto_front_fct, problem_title,"f1" ,"f2", sleep=sleeptime)

    #return the approximation of the pareto front and the archive if managed
    return result



#algorithm that show on a animated graph the evolution of a population to get a pareto front
def getFrontParetoWithoutGraphic(start_fct, operator_fct, generation_fct, nb_functions,
               nb_iterations, neighboring_size, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, manage_archive, nb_samples, training_neighborhood_size, strategy, file_to_write, filter_strat, free_eval, param_print_every, file_to_writeR2, filenameDIR, filenameSCORE, sleeptime=10):
    global param, archiveOK

    if(manage_archive):
        archiveOK = True
    #random initialisation
    init_decisions = init_to.initRandom(generation_fct, nb_functions, problem_size, search_space)
    #algorithm parameters
    param = [start_fct, nb_functions, nb_iterations, neighboring_size, init_decisions, problem_size, max_decisions_maj, delta_neighbourhood, CR, search_space, F, distrib_index_n, pm, operator_fct, nb_samples, training_neighborhood_size, strategy, file_to_write, filter_strat, free_eval, param_print_every, file_to_writeR2, filenameDIR, filenameSCORE]
    #function that will be called by runAnimatedGraph before it's end
    end_function = getResult
    #launch the graphic view and the algorithm
    result = runTcheby()

    #return the approximation of the pareto front and the archive if managed
    return result



def runTcheby():
    global param, approx_pareto_front, archiveOK, NO_FILE_TO_WRITE

    ############################################################################
    # PARAMETER

    #clf = SVR(C=1.0, epsilon=0.1, kernel="rbf")
    clf = RandomForestRegressor()
    clf2 = -1
    two_models_bool = False

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
    param_print_every, file_to_writeR2     = param[20:22]
    filenameDIR, filenameSCORE             = param[22:24]

    nb_objectives = len(start_fct)

    #get separatly offspring operator fct
    crossover_fct, mutation_fct, repair_fct = operator_fct

    best_decisions = copy.deepcopy(init_decisions)

    sampling_param = [crossover_fct, mutation_fct, repair_fct, best_decisions, F, problem_size, CR, search_space, distrib_index_n, pm]


    ############################################################################
    # INITIALISATION

    qual_tools.resetGlobalVariables(filenameDIR, filenameSCORE, nb_iterations, nb_functions)

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

    #get the first training part of the item we will learn on
    model_directions = train_to.getDirectionsTrainingMatrix(directions)

    #if the data shall be write in a file
    writeOK = False
    if(file_to_write != NO_FILE_TO_WRITE):
        writeOK = True

    writeR2OK = False
    if(file_to_writeR2 != NO_FILE_TO_WRITE):
        writeR2OK = True

    ############################################################################
    # MAIN ALGORITHM

    if(writeOK):
        iot.printObjectives(file_to_write, eval_to.getNbEvals(), 0,best_decisions_scores, problem_size, nb_objectives)

    #IDs tab to allow a random course through the directions in the main loop
    id_directions = [i for i in range(nb_functions)]

    #iterations loop
    for itera in range(nb_iterations):
        if(not free_eval):
            #Update model
            training_inputs, training_outputs, training_set_size, training_scores = train_to.getTrainingSet(model_directions, best_decisions, best_decisions_scores ,eval_to.getZstar_with_decal(), strategy, nb_functions, training_neighborhood_size)

            clf.fit(training_inputs, training_outputs)

        '''
        if(writeR2OK and not free_eval):
            training_inputs_tcheby      = eval_to.getManyTcheby(training_inputs, training_scores, eval_to.getZstar_with_decal(), training_set_size)

            random_index = numpy.arange(0,training_set_size)
            numpy.random.shuffle(random_index)
            n_folds = 10
            folds_sizes = (training_set_size // n_folds) * numpy.ones(n_folds, dtype=numpy.int)
            folds_sizes[:training_set_size % n_folds] += 1

            training_inputs_array = numpy.array(training_inputs)
            training_tcheby_array = numpy.array(training_inputs_tcheby)

            R2_cv = []
            MSE_cv = []
            MAE_cv = []
            MDAE_cv = []

            clfCV = RandomForestRegressor()

            current = 0
            for fold_size in folds_sizes:
                start, stop = current, current + fold_size
                mask = numpy.ones(training_set_size, dtype=bool)
                mask[start:stop] = 0
                current = stop

                clfCV.fit(training_inputs_array[random_index[mask]], training_tcheby_array[random_index[mask]])

                test_fold_tcheby = training_tcheby_array[random_index[start:stop]]
                test_fold_predict = clfCV.predict(training_inputs_array[random_index[start:stop]])

                R2_cv  .append(r2_score             (test_fold_tcheby, test_fold_predict))
                MSE_cv .append(mean_squared_error   (test_fold_tcheby, test_fold_predict))
                MAE_cv .append(mean_absolute_error  (test_fold_tcheby, test_fold_predict))
                MDAE_cv.append(median_absolute_error(test_fold_tcheby, test_fold_predict))

            R2 = clf.score(training_inputs, training_outputs)
            MSE_cv_mean = numpy.mean(MSE_cv)
            RMSE_cv_mean = math.sqrt(MSE_cv_mean)
            MAE_cv_mean = numpy.mean(MAE_cv)
            MDAE_cv_mean = numpy.mean(MDAE_cv)
            R2_cv_mean = numpy.mean(R2_cv)

            iot.printR2(file_to_writeR2, eval_to.getNbEvals(), itera,  R2, R2_cv_mean, MSE_cv_mean , MAE_cv_mean, MDAE_cv_mean, RMSE_cv_mean, problem_size, print_every=1)
        '''
        #random course through the directions
        random.shuffle(id_directions)

        #functions loop
        for f in id_directions:

            #get all the indice of neighbors of a function in a certain distance of f and include f in
            f_neighbors, current_neighbourhing_size = nt.getNeighborsOf(f, delta_neighbourhood)

            #get a list of offspring from the neighbors
            list_offspring = samp_to.extended_sampling(f, f_neighbors, sampling_param, nb_samples)

            #apply a filter on the offspring list and select the best one
            filter_param = [itera, f, clf, clf2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, eval_to.getZstar_with_decal(), best_decisions_scores, best_decisions, nb_objectives]
            best_candidate = filt_to.model_based_filtring(filter_strat, free_eval, filter_param)

            #evaluation of the newly made solution
            mix_scores = eval_to.eval(start_fct, best_candidate, problem_size)

            #MAJ of the z_star point
            has_changed = eval_to.min_update_Z_star(mix_scores, nb_objectives)

            #retraining of the model with the new z_star
            if(has_changed and not free_eval):
                train_to.updateTrainingZstar(eval_to.getZstar_with_decal())
                training_outputs = train_to.retrainSet(training_inputs, training_scores, eval_to.getZstar_with_decal(), training_set_size, nb_objectives)
                clf.fit(training_inputs, training_outputs)

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
                wj = (directions[0][j],directions[1][j])
                g_mix = eval_to.g_tcheby(wj, mix_scores, eval_to.getZstar_with_decal())
                g_best = eval_to.g_tcheby(wj, best_decisions_scores[j], eval_to.getZstar_with_decal())

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
            iot.printObjectives(file_to_write, eval_to.getNbEvals(), itera+1, best_decisions_scores, problem_size, nb_objectives, print_every=param_print_every)
            continue

        #graphic update
        #yield arch_to.getArchiveScore(), best_decisions_scores, itera+1, eval_to.getNbEvals(), eval_to.getZstar_with_decal(), pop_size, isReals
    if(not free_eval and writeR2OK):
        qual_tools.computeQualityEvaluation()
        qual_tools.generateDiffPredFreeFile()
    return
