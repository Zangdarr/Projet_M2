import numpy as np
import random
import evaluation_tools as eval_to
import model_quality_tools as qual_to
import training_tools as train_to

MAX_INTEGER = 2**30

#--------------------------------------------------------------------------------------------------------------
# MODEL-BASED-FILTRING

def model_based_filtring(filter_strat, free_eval,  param):

    if(filter_strat == 'AvScl'):
        return AverageScalar(free_eval, param, False, False)
    elif(filter_strat == 'AvSclNormG'):
        return AverageScalar(free_eval, param, True, True)
    elif(filter_strat == 'AvSclNormP'):
        return AverageScalar(free_eval, param, True, False)
    elif(filter_strat == 'best'):
        return best_score(free_eval, param)
    elif(filter_strat == 'AvImprG'):
        return AverageImprovement(free_eval, param, False, True)
    elif(filter_strat == 'AvImprP'):
        return AverageImprovement(free_eval, param, False, False)
    elif(filter_strat == 'AvImprNormG'):
        return AverageImprovement(free_eval, param, True, True)
    elif(filter_strat == 'AvImprNormP'):
        return AverageImprovement(free_eval, param, True, False)
    elif(filter_strat == 'bestdiff'):
        return bestdiff_score(free_eval, param)
    elif(filter_strat == 'by_direction'):
        return by_direction_score(free_eval, param)
    elif(filter_strat == 'numberdir'):
        return numberdir_score(free_eval, param)


#Return a candidat randomly selected within those that improve the maximum of direction within the current direction neighborhood
def numberdir_score(free_eval, param):

    current_g, current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores, population_indiv = param


    id_offspring = -1
    offspring_result_pred = []
    offspring_result_free = []

    for offspring in list_offspring:
        id_offspring += 1
        numberdir_score_pred = 0
        numberdir_score_free = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data_pred = np.matrix(f_input_data)
           f = 0
           for data in f_input_data_pred:
               tmp_pred = predict_and_quality(model, f_input_data[f], data, start_fct, problem_size, current_g, f_neighbors[f])
               tmp_free = computeTchebyFreeEval(f_input_data[f], start_fct, problem_size, z_star)
               current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)
               if(current_gtcheby > tmp_pred):
                   numberdir_score_pred += 1
               if(current_gtcheby > tmp_free):
                   numberdir_score_free += 1

               f +=1
           offspring_result_pred.append(numberdir_score_pred)
        else:
            f = 0
            for data in f_input_data:
                tmp_free = computeTchebyFreeEval(data, start_fct, problem_size, z_star)
                current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0] , population_scores[f_neighbors[f]], z_star)
                if(current_gtcheby > tmp_free):
                    numberdir_score_free += 1
                f +=1

        offspring_result_free.append(numberdir_score_free)

    score_best_free = max(offspring_result_free)
    best_indexes_free = [i for i, j in enumerate(offspring_result_free) if j == score_best_free]
    choice_free = random.choice(best_indexes_free)

    choice = -1
    if(free_eval):
        choice = choice_free
    else:
        score_best_pred = max(offspring_result_pred)
        best_indexes_pred = [i for i, j in enumerate(offspring_result_pred) if j == score_best_pred]
        choice_pred = random.choice(best_indexes_pred)
        save_best_free_pred_score = offspring_result_pred[choice_free]
        save_best_pred_free_score = offspring_result_free[choice_pred]
        choice = choice_pred
        diffFreePredict(current_g, current_f, score_best_pred, save_best_pred_free_score, choice_pred, score_best_free, save_best_free_pred_score,  choice_free)

    return list_offspring[choice]


#Return the candidat the minimizes the score only for the current direction
def by_direction_score(free_eval, param):
    global MAX_INTEGER

    current_g, current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores, population_indiv = param

    id_offspring = -1
    index_best_pred = -1
    index_best_free = -1
    score_best_pred = MAX_INTEGER
    score_best_free = MAX_INTEGER
    save_best_pred_free_score = MAX_INTEGER
    save_best_free_pred_score = MAX_INTEGER

    current_f_w = model_directions[current_f].tolist()[0]

    for offspring in list_offspring:
        id_offspring += 1
        tmp_free = -1
        tmp_pred = -1

        f_input_data = []

        f_input_data.extend(current_f_w)

        f_input_data.extend(offspring)

        if(not free_eval):
           f_input_data_pred = np.matrix(f_input_data)
           tmp_pred = predict_and_quality(model, f_input_data, f_input_data_pred, start_fct, problem_size, current_g, current_f)
           score_eval = eval_to.free_eval(start_fct, offspring, problem_size)
           tmp_free = eval_to.g_tcheby(current_f_w, score_eval, z_star)

           if(index_best_pred == -1):
               index_best_pred = id_offspring
               score_best_pred = tmp_pred
               save_best_pred_free_score = tmp_free
           elif(tmp_pred < score_best_pred):
               index_best_pred = id_offspring
               score_best_pred = tmp_pred
               save_best_pred_free_score = tmp_free
           else:
               pass

        if(free_eval):
            score_eval = eval_to.free_eval(start_fct, offspring, problem_size)
            tmp_free = eval_to.g_tcheby(current_f_w, score_eval, z_star)

        if(index_best_free == -1):
            index_best_free = id_offspring
            score_best_free = tmp_free
            save_best_free_pred_score = tmp_pred
        elif(tmp_free < score_best_free):
            index_best_free = id_offspring
            score_best_free = tmp_free
            save_best_free_pred_score = tmp_pred
        else :
            pass

    index_best = -1
    if(free_eval):
        index_best = index_best_free
    else :
        index_best = index_best_pred
        diffFreePredict(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score,  index_best_free)


    return list_offspring[index_best]


#Return the candidate that maximise the improvement among the direction of the current direction neighborhood
def bestdiff_score(free_eval, param):

    current_g, current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores, population_indiv = param


    id_offspring = -1
    index_best_pred = -1
    score_best_pred = -1 * MAX_INTEGER
    save_best_pred_free_score = -1
    index_best_free = -1
    score_best_free = -1 * MAX_INTEGER
    save_best_free_pred_score = -1
    for offspring in list_offspring:
        id_offspring += 1
        diff_score_pred = -1 * MAX_INTEGER
        diff_score_free = -1 * MAX_INTEGER

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data_for_pred = np.matrix(f_input_data)
           f = 0
           for data in f_input_data_for_pred:
               tmp_pred = predict_and_quality(model, f_input_data[f], data, start_fct, problem_size, current_g, f_neighbors[f])
               tmp_free = computeTchebyFreeEval(f_input_data[f], start_fct, problem_size, z_star)
               current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)
               diff_score_pred = max(diff_score_pred, current_gtcheby - tmp_pred)
               diff_score_free = max(diff_score_free, current_gtcheby - tmp_free)
               f +=1

           if(index_best_pred == -1):
                 index_best_pred = id_offspring
                 score_best_pred = diff_score_pred
                 save_best_pred_free_score = diff_score_free
           elif(diff_score_pred > score_best_pred):
                 index_best_pred = id_offspring
                 score_best_pred = diff_score_pred
                 save_best_pred_free_score = diff_score_free
           else :
                 pass
        else:
            f = 0
            for data in f_input_data:
                tmp_free = computeTchebyFreeEval(data, start_fct, problem_size, z_star)
                current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0] , population_scores[f_neighbors[f]], z_star)
                diff_score_free = max(diff_score_free, current_gtcheby - tmp_free)
                f +=1

        if(index_best_free == -1):
            index_best_free = id_offspring
            score_best_free = diff_score_free
            save_best_free_pred_score = diff_score_pred
        elif(diff_score_free > score_best_free):
            index_best_free = id_offspring
            score_best_free = diff_score_free
            save_best_free_pred_score = diff_score_pred
        else :
            pass

    index_best = -1
    if(free_eval):
         index_best = index_best_free
    else:
         diffFreePredict(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score,  index_best_free)

         index_best = index_best_pred

    return list_offspring[index_best]


#Return the candidat with the maximun average scalar improvement over the direction within the current direction neighborhood
def AverageImprovement  (free_eval, param, normalize, withTruescore):

    current_g, current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores, population_indiv = param


    id_offspring = -1
    index_best_pred = -1
    score_best_pred = 0
    save_best_pred_free_score = -1
    index_best_free = -1
    score_best_free = 0
    save_best_free_pred_score = -1
    for offspring in list_offspring:
        id_offspring += 1
        diff_score_pred = 0
        diff_score_free = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data_pred = np.matrix(f_input_data)
           f = 0
           for data in f_input_data_pred:
               tmp_pred = predict_and_quality(model, f_input_data[f], data, start_fct, problem_size, current_g, f_neighbors[f])
               tmp_free = computeTchebyFreeEval(f_input_data[f], start_fct, problem_size, z_star)
               current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)
               if(withTruescore):
                    if(normalize):
                        diff_score_pred += max(0, (current_gtcheby - tmp_pred) / current_gtcheby )
                        diff_score_free += max(0, (current_gtcheby - tmp_free) / current_gtcheby )
                    else:
                        diff_score_pred += max(0, current_gtcheby - tmp_pred)
                        diff_score_free += max(0, current_gtcheby - tmp_free)
               else:

                   current_pred = model.predict([f_input_data[f][0:2] + population_indiv[f_neighbors[f]]])[0]
                   if(normalize):
                       diff_score_pred += max(0, (current_pred - tmp_pred) / current_pred )
                       diff_score_free += max(0, (current_pred - tmp_free) / current_pred )
                   else:
                       diff_score_pred += max(0, current_pred - tmp_pred)
                       diff_score_free += max(0, current_pred - tmp_free)
               f +=1

           diff_score_pred /= float(f)
           diff_score_free /= float(f)
           if(index_best_pred == -1):
                 index_best_pred = id_offspring
                 score_best_pred = diff_score_pred
                 save_best_pred_free_score = diff_score_free
           elif(diff_score_pred > score_best_pred):
                 index_best_pred = id_offspring
                 score_best_pred = diff_score_pred
                 save_best_pred_free_score = diff_score_free
           else :
                 pass
        else:
            f = 0
            for data in f_input_data:
                tmp_free = computeTchebyFreeEval(data, start_fct, problem_size, z_star)
                current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0] , population_scores[f_neighbors[f]], z_star)
                if(normalize):
                    diff_score_free += max(0, (current_gtcheby - tmp_free) / current_gtcheby )
                else:
                    diff_score_free += max(0, current_gtcheby - tmp_free)
                f +=1
            diff_score_free /= float(f)

        if(index_best_free == -1):
            index_best_free = id_offspring
            score_best_free = diff_score_free
            save_best_free_pred_score = diff_score_pred
        elif(diff_score_free > score_best_free):
            index_best_free = id_offspring
            score_best_free = diff_score_free
            save_best_free_pred_score = diff_score_pred
        else :
            pass

    index_best = -1
    if(free_eval):
         index_best = index_best_free
    else:
         diffFreePredict(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score,  index_best_free)

         index_best = index_best_pred

    return list_offspring[index_best]


#Return the candidat that minimizes the score among the direction within the neighborhood of the current direction
def best_score(free_eval, param):
    global MAX_INTEGER

    current_g, current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores, population_indiv = param


    id_offspring = -1
    index_best_pred = -1
    score_best_pred = MAX_INTEGER
    save_best_pred_free_score = -1
    index_best_free = -1
    score_best_free = MAX_INTEGER
    save_best_free_pred_score = -1
    for offspring in list_offspring:
        id_offspring += 1
        min_score_pred = MAX_INTEGER
        min_score_free = MAX_INTEGER
        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data_pred = np.matrix(f_input_data)
           f = 0
           for data in f_input_data_pred:
               tmp_pred = predict_and_quality(model, f_input_data[f], data, start_fct, problem_size, current_g, f_neighbors[f])
               tmp_free = computeTchebyFreeEval(f_input_data[f], start_fct, problem_size, z_star)
               min_score_pred = min(tmp_pred, min_score_pred)
               min_score_free = min(tmp_free, min_score_free)

               f +=1
           if(index_best_pred == -1):
                index_best_pred = id_offspring
                score_best_pred = min_score_pred
                save_best_pred_free_score = min_score_free
           elif(min_score_pred < score_best_pred):
                index_best_pred = id_offspring
                score_best_pred = min_score_pred
                save_best_pred_free_score = min_score_free
           else :
                pass

        else:
            for data in f_input_data:
                tmp_free = computeTchebyFreeEval(data, start_fct, problem_size, z_star)
                min_score_free = min(tmp_free, min_score_free)

        if(index_best_free == -1):
            index_best_free = id_offspring
            score_best_free = min_score_free
            save_best_free_pred_score = min_score_pred
        elif(min_score_free < score_best_free):
            index_best_free = id_offspring
            score_best_free = min_score_free
            save_best_free_pred_score = min_score_pred
        else :
            pass

    index_best = -1
    if(free_eval):
         index_best = index_best_free
    else:
         diffFreePredict(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score,  index_best_free)

         index_best = index_best_pred

    return list_offspring[index_best]


#Return the candidate that minimizes the average score over the neighborhood of the current direction.
def AverageScalar(free_eval, param, normalize, withTruescore):
    global MAX_INTEGER

    current_g, current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores, population_indiv = param


    id_offspring = -1
    index_best_pred = -1
    score_best_pred = MAX_INTEGER
    save_best_pred_free_score = -1
    index_best_free = -1
    score_best_free = MAX_INTEGER
    save_best_free_pred_score = -1
    for offspring in list_offspring:
        id_offspring += 1
        average_score_pred = 0
        average_score_free = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        count = 0
        if(not free_eval):
           f_input_data_pred = np.matrix(f_input_data)
           f = 0
           for data in f_input_data_pred:
               tmp_pred = predict_and_quality(model, f_input_data[f], data, start_fct, problem_size, current_g, f_neighbors[f])
               tmp_free = computeTchebyFreeEval(f_input_data[f], start_fct, problem_size, z_star)
               if(normalize):
                   if(withTruescore):
                       current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)
                       average_score_pred += ( tmp_pred / current_gtcheby )
                       average_score_free += ( tmp_free / current_gtcheby )
                   else:
                       current_pred = model.predict([f_input_data[f][0:2] + population_indiv[f_neighbors[f]]])[0]
                       average_score_pred += ( tmp_pred / current_pred )
                       average_score_free += ( tmp_free / current_pred )
               else:
                   average_score_pred += tmp_pred
                   average_score_free += tmp_free
               count +=1
               f +=1

           average_score_pred /= float(count)
           average_score_free /= float(count)
           if(index_best_pred == -1):
                index_best_pred = id_offspring
                score_best_pred = average_score_pred
                save_best_pred_free_score = average_score_free
           elif(average_score_pred < score_best_pred):
                index_best_pred = id_offspring
                score_best_pred = average_score_pred
                save_best_pred_free_score = average_score_free
           else :
                pass

        else: # free_eval
            f = 0
            for data in f_input_data:
                tmp_free = computeTchebyFreeEval(data, start_fct, problem_size, z_star)
                if(normalize):
                    current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)
                    average_score_free += ( tmp_free / current_gtcheby )
                else:# normalize false
                    average_score_free += tmp_free
                count +=1
                f += 1
            average_score_free /= float(count)

        if(index_best_free == -1):
            index_best_free = id_offspring
            score_best_free = average_score_free
            save_best_free_pred_score = average_score_pred
        elif(average_score_free < score_best_free):
            index_best_free = id_offspring
            score_best_free = average_score_free
            save_best_free_pred_score = average_score_pred
        else :
            pass

    index_best = -1
    if(free_eval):
         index_best = index_best_free
    else:
         diffFreePredict(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score,  index_best_free)

         index_best = index_best_pred

    return list_offspring[index_best]


def getInputData(f_neighbors, model_directions, offspring):
    l= []
    id_l = -1
    for i in f_neighbors:
        id_l += 1
        l.append([])

        l[id_l].extend(model_directions[i].tolist()[0])

        l[id_l].extend(offspring)

    return l


def computeTchebyFreeEval(data, start_fct, problem_size, z_star):
    w = data[0:2]
    offs = data[2:]
    score_eval = eval_to.free_eval(start_fct, offs, problem_size)
    return eval_to.g_tcheby(w, score_eval, z_star)

def predict_and_quality(model, data_free, data_pred, start_fct, problem_size, g, d):
    w = data_free[0:2]
    offs = data_free[2:]
    score_freeeval = eval_to.free_eval(start_fct, offs, problem_size)
    tcheby_freeeval = eval_to.g_tcheby(w, score_freeeval, train_to.getTrainingZstar())
    tcheby_predict  = model.predict(data_pred)
    qual_to.add(g, d, tcheby_predict[0], tcheby_freeeval)
    return tcheby_predict[0]

def diffFreePredict(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score, index_best_free):
    qual_to.addToScoreTab(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score, index_best_free)
