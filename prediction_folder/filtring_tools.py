import numpy as np
import random
import evaluation_tools as eval_to
import model_quality_tools as qual_to
import training_tools as train_to

MAX_INTEGER = 2**30

#--------------------------------------------------------------------------------------------------------------
# MODEL-BASED-FILTRING

def model_based_filtring(filter_strat, free_eval,  param):

    if(filter_strat == 'average'):
        return average_score(free_eval, param)
    elif(filter_strat == 'best'):
        return best_score(free_eval, param)
    elif(filter_strat == 'maxdiff'):
        return maxdiff_score(free_eval, param)
    elif(filter_strat == 'bestdiff'):
        return bestdiff_score(free_eval, param)
    elif(filter_strat == 'by_direction'):
        return by_direction_score(free_eval, param)
    elif(filter_strat == 'numberdir'):
        return numberdir_score(free_eval, param)


#Return a candidat randomly selected within those that improve the maximum of direction within the current direction neighborhood
def numberdir_score(free_eval, param):

    current_g, current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


    id_offspring = -1
    offspring_result = []

    for offspring in list_offspring:
        id_offspring += 1
        numberdir_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data_pred = np.matrix(f_input_data)
           f = 0
           for data in f_input_data_pred:
               tmp = predict_and_quality(model, f_input_data[f], data, start_fct, problem_size, current_g, f_neighbors[f])
               current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)
               if(current_gtcheby > tmp):
                   numberdir_score += 1
               f +=1
        else:
            f = 0
            for data in f_input_data:
                w = data[0:2]
                offs = data[2:]
                score_eval = eval_to.free_eval(start_fct, offs, problem_size)
                tmp = eval_to.g_tcheby(w, score_eval, z_star)
                current_gtcheby = eval_to.g_tcheby(w , population_scores[f_neighbors[f]], z_star)
                if(current_gtcheby > tmp):
                    numberdir_score += 1
                f +=1

        offspring_result.append(numberdir_score)

    score_best = max(offspring_result)
    best_indexes = [i for i, j in enumerate(offspring_result) if j == score_best]
    choice = random.SystemRandom().choice(best_indexes)

    return list_offspring[choice]


#Return the candidat the minimizes the score only for the current direction
def by_direction_score(free_eval, param):

    current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param
    id_offspring = -1
    index_best = -1
    score_best = 0

    current_f_w = model_directions[current_f].tolist()[0]

    for offspring in list_offspring:
        id_offspring += 1
        diff_score = 0

        f_input_data = []

        f_input_data.extend(current_f_w)

        f_input_data.extend(offspring)

        if(not free_eval):
           f_input_data = np.matrix(f_input_data)
           tmp = model.predict(f_input_data)

        if(free_eval):
            score_eval = eval_to.free_eval(start_fct, offspring, problem_size)
            tmp = eval_to.g_tcheby(current_f_w, score_eval, z_star)

        if(index_best == -1):
            index_best = id_offspring
            score_best = tmp
        elif(tmp < score_best):
            index_best = id_offspring
            score_best = tmp
        else :
            pass
    return list_offspring[index_best]


#Return the candidate that maximise the improvement among the direction of the current direction neighborhood
def bestdiff_score(free_eval, param):

    current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


    id_offspring = -1
    index_best = -1
    score_best = 0

    for offspring in list_offspring:
        id_offspring += 1
        diff_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data = np.matrix(f_input_data)

        f = 0
        for data in f_input_data:
            if(free_eval):
                w = data[0:2]
                offs = data[2:]
                score_eval = eval_to.free_eval(start_fct, offs, problem_size)
                tmp = eval_to.g_tcheby(w, score_eval, z_star)
                current_gtcheby = eval_to.g_tcheby(w , population_scores[f_neighbors[f]], z_star)
            else:
                tmp = model.predict(data)
                current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)

            diff_score = max(0, current_gtcheby - tmp)
            f +=1


            if(index_best == -1):
                index_best = id_offspring
                score_best = diff_score
            elif(diff_score > score_best):
                index_best = id_offspring
                score_best = diff_score
            else :
                pass

    return list_offspring[index_best]


#Return the candidat with the maximun average scalar improvement over the direction within the current direction neighborhood
def maxdiff_score(free_eval, param):

    current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


    id_offspring = -1
    index_best = -1
    score_best = 0

    for offspring in list_offspring:
        id_offspring += 1
        diff_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data = np.matrix(f_input_data)

        f = 0
        for data in f_input_data:
            if(free_eval):
                w = data[0:2]
                offs = data[2:]
                score_eval = eval_to.free_eval(start_fct, offs, problem_size)
                tmp = eval_to.g_tcheby(w, score_eval, z_star)
                current_gtcheby = eval_to.g_tcheby(w , population_scores[f_neighbors[f]], z_star)
            else:
                tmp = model.predict(data)
                current_gtcheby = eval_to.g_tcheby(model_directions[f_neighbors[f]].tolist()[0], population_scores[f_neighbors[f]], z_star)
            diff_score += max(0, current_gtcheby - tmp)
            f +=1

        if(index_best == -1):
            index_best = id_offspring
            score_best = diff_score
        elif(diff_score > score_best):
            index_best = id_offspring
            score_best = diff_score
        else :
            pass

    return list_offspring[index_best]


#Return the candidat that minimizes the score among the direction within the neighborhood of the current direction
def best_score(free_eval, param):
    global MAX_INTEGER

    current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


    id_offspring = -1
    index_best = -1
    score_best = MAX_INTEGER
    for offspring in list_offspring:
        id_offspring += 1
        min_score = MAX_INTEGER

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data = np.matrix(f_input_data)


        for data in f_input_data:
            if(free_eval):
                w = data[0:2]
                offs = data[2:]
                score_eval = eval_to.free_eval(start_fct, offs, problem_size)
                tmp = eval_to.g_tcheby(w, score_eval, z_star)
            else:
                tmp = model.predict(data)

            min_score = min(tmp, min_score)


        if(index_best == -1):
            index_best = id_offspring
            score_best = min_score
        elif(min_score < score_best):
            index_best = id_offspring
            score_best = min_score
        else :
            pass

    return list_offspring[index_best]


#Return the candidate that minimizes the average score over the neighborhood of the current direction.
def average_score(free_eval, param):
    global MAX_INTEGER

    current_f, model, model2, two_models_bool, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


    id_offspring = -1
    index_best = -1
    score_best = MAX_INTEGER
    for offspring in list_offspring:
        id_offspring += 1
        average_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval and not two_models_bool):
           f_input_data = np.matrix(f_input_data)

        count = 0
        for data in f_input_data:
            if(free_eval):
                w = data[0:2]
                offs = data[2:]
                score_eval = eval_to.free_eval(start_fct, offs, problem_size)
                tmp = eval_to.g_tcheby(w, score_eval, z_star)
            elif(not two_models_bool):
                tmp = model.predict(data)
            else:#2 models

                offs = data[2:]

                e1 = model.predict(np.array(offs).reshape(1,-1)).tolist()
                e2 = model2.predict(np.array(offs).reshape(1,-1)).tolist()

                scores = [e1[0], e2[0]]
                w = data[0:2]
                tmp = eval_to.g_tcheby(w, scores, z_star)

            average_score += tmp
            count +=1

        average_score /= float(count)
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

    return l
