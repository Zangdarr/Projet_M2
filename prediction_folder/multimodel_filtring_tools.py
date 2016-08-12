import numpy as np
import random
import evaluation_tools as eval_to
import multimodel_quality_tools as qual_to

######Main

# Main function that perform the filtring of the set of offprings and return the best candidate according to the score function used.
def filter_function(scorefunction_name, param):

    # parameters splitting
    main_g, main_f, model_tab, neighborhood_indexlist, offspring_list, main_weightvectors, objective_functions, problem_size, z_star, population_scores, population_indiv, objective_quantity = param

    # get the weight vectors regarding the current neighborhood
    neighborhood_weightvectors = getNeighborhoodWeightVectors(neighborhood_indexlist, main_weightvectors)

    # get the objective vectors by applying the prediction of the models on the offsprings
    pred_objectivevectors = applyPredictions(model_tab, offspring_list, objective_quantity)

    # get the objective vectors by applying free evaluation on the offsprings
    free_objectivevectors = applyFreeevals(offspring_list, objective_functions, problem_size)

    # quality measurement (DIR file, DIRSTAR file)
    qual_to.add(main_g, main_f, pred_objectivevectors, free_objectivevectors, objective_quantity)

    # get the scores with the score function specify in parameter for all the offsprings in the list
    pred_scores, free_scores, bestindividualidselection_function = applyScoreFunction(scorefunction_name, pred_objectivevectors, free_objectivevectors, neighborhood_weightvectors, objective_quantity, z_star)

    # get the best index for pred and free, if there is equality then random choice between the best ones
    pred_bestindex, free_bestindex = bestindividualidselection_function(pred_scores, free_scores)

    # quality measurement (SCORE file)
    diffFreePredict(main_g, main_f, pred_bestindex, free_bestindex, pred_scores, free_scores)

    # return the best offspring
    return offspring_list[pred_bestindex]


######Sub-functions of the main one

# Provide the weight vectors belongings to the neighborhood
def getNeighborhoodWeightVectors(neighborhood_indexlist, main_weightvectors):
    return main_weightvectors[neighborhood_indexlist].tolist()

# Apply the prediction of all the models in model_tab on the offsprings list
def applyPredictions(model_tab, offspring_list, objective_quantity):
    prediction_tab = []

    for i in range(0, objective_quantity):
        current_model = model_tab[i]
        current_tmp   = current_model.predict(offspring_list)
        prediction_tab.append(current_tmp)

    return prediction_tab

# Apply free evalution on the offsprings
def applyFreeevals(offspring_list, objective_functions, problem_size):
    freeeval_tab =[]

    for offspring in offspring_list:
        current_tmp = eval_to.free_eval(objective_functions, offspring, problem_size)
        freeeval_tab.append(current_tmp)

    return freeeval_tab

# Apply the score function on the objective vectors and return their scores
def applyScoreFunction(scorefunction_name, pred_objectivevectors, free_objectivevectors, neighborhood_weightvectors, objective_quantity, z_star):
    #score function to be use
    current_scorefunction, current_bestindividualidselectionfunction = getScoreFunction(scorefunction_name)

    #compute the size of the current neighborhood
    neighborhood_size = float(len(neighborhood_weightvectors))

    #compute the size of the current objective vectors
    objectivevector_size = len(free_objectivevectors)

    #records of the score of each offspring
    offspring_predbasedscore = []
    offspring_freebasedscore = []

    #for each offspring
    for loop_offid in range(0, objectivevector_size):
        # get objective vector
        current_freeobjvector = free_objectivevectors[loop_offid]
        current_predobjvector = [pred_objectivevectors[loop_tmp][loop_offid] for loop_tmp in range(objective_quantity)]

        # compute the score function
        current_predscore, current_freescore = current_scorefunction(current_predobjvector, current_freeobjvector, neighborhood_weightvectors, objective_quantity, z_star, neighborhood_size)

        # record it in the results tab
        offspring_predbasedscore.append(current_predscore)
        offspring_freebasedscore.append(current_freescore)

    #return the results tab
    return offspring_predbasedscore, offspring_freebasedscore, current_bestindividualidselectionfunction

# Return the index of the best individual according to the scores for a minimization problem
def getBestIndividualId_MinimizationProblem(pred_scores, free_scores):
    #get scores minimale value
    pred_minscore = min(pred_scores)
    free_minscore = min(free_scores)

    #get individuals ids that score the minimal value
    pred_bestindividualidlist = [i for i, j in enumerate(pred_scores) if j == pred_minscore]
    free_bestindividualidlist = [i for i, j in enumerate(free_scores) if j == free_minscore]

    #select randomly one individual among those with the minimal value
    pred_bestindividualid = random.choice(pred_bestindividualidlist)
    free_bestindividualid = random.choice(free_bestindividualidlist)

    #return the two best selected
    return pred_bestindividualid, free_bestindividualid

# Return the index of the best individual according to the scores for a maximization problem
def getBestIndividualId_MaximizationProblem(pred_scores, free_scores):
    #get scores maximale value
    pred_maxscore = max(pred_scores)
    free_maxscore = max(free_scores)

    #get individuals ids that score the minimal value
    pred_bestindividualidlist = [i for i, j in enumerate(pred_scores) if j == pred_maxscore]
    free_bestindividualidlist = [i for i, j in enumerate(free_scores) if j == free_maxscore]

    #select randomly one individual among those with the minimal value
    pred_bestindividualid = random.choice(pred_bestindividualidlist)
    free_bestindividualid = random.choice(free_bestindividualidlist)

    #return the two best selected
    return pred_bestindividualid, free_bestindividualid


######Sub-functions of the subfunctions

# Provide the score function to be use according to the score function name given in parameter
def getScoreFunction(scorefunction_name):
    if(scorefunction_name == "AvScl"):
        return scorefunction_AverageScalar, getBestIndividualId_MinimizationProblem


######Score functions

# Apply the score function AverageScalar on an objective vector and return the scores and the function to use to get the best id
def scorefunction_AverageScalar(current_predobjvector, current_freeobjvector, neighborhood_weightvectors, objective_quantity, z_star, neighborhood_size):
    #scores
    current_predscoresum = 0.0
    current_freescoresum = 0.0

    #for each weight vector
    for current_weightvector in neighborhood_weightvectors:
        # get tchebycheff for the current weight vector
        current_predtcheby = eval_to.g_tcheby(current_weightvector, current_predobjvector, z_star)
        current_freetcheby = eval_to.g_tcheby(current_weightvector, current_freeobjvector, z_star)
        # sum for average
        current_predscoresum += current_predtcheby
        current_freescoresum += current_freetcheby

    #ponderation of the sums to get the average scores
    pred_averagescore = current_predscoresum / neighborhood_size
    free_averagescore = current_freescoresum / neighborhood_size

    #return the scores
    return pred_averagescore, free_averagescore


#####Quality measurement functions

def diffFreePredict(g, f, pred_bestindex, free_bestindex, pred_scores, free_scores):
    score_best_pred           = pred_scores[pred_bestindex]
    save_best_pred_free_score = free_scores[pred_bestindex]
    score_best_free           = free_scores[free_bestindex]
    save_best_free_pred_score = pred_scores[free_bestindex]

    qual_to.addToScoreTab(g, f, score_best_pred, save_best_pred_free_score, pred_bestindex, score_best_free, save_best_free_pred_score, free_bestindex)