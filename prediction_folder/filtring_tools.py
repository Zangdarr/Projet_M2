import numpy as np

import evaluation_tools as eval_to

MAX_INTEGER = 2**30

#--------------------------------------------------------------------------------------------------------------
# MODEL-BASED-FILTRING

def model_based_filtring(filter_strat, free_eval,  param):

    if(filter_strat == 'average'):
        return average_model_based(free_eval, param)
    elif(filter_strat == 'min'):
        return min_model_based(free_eval, param)
    elif(filter_strat == 'maxdiff'):
        return maxdiff_model_based(free_eval, param)

#moyenne des écart
def maxdiff_model_based(free_eval, param):

    model, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


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
                current_gtcheby = eval_to.g_tcheby(w , population_scores[f], z_star)
            else:
                tmp = model.predict(data)
                current_gtcheby = eval_to.g_tcheby(model_directions[f].tolist()[0], population_scores[f], z_star)

            diff_score += current_gtcheby - tmp
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


def min_model_based(free_eval, param):
    global MAX_INTEGER

    model, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


    id_offspring = -1
    index_best = -1
    score_best = 0
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


def average_model_based(free_eval, param):

    model, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star, population_scores = param


    id_offspring = -1
    index_best = -1
    score_best = 0
    for offspring in list_offspring:
        id_offspring += 1
        average_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        if(not free_eval):
           f_input_data = np.matrix(f_input_data)

        count = 0
        for data in f_input_data:
            if(free_eval):
                w = data[0:2]
                offs = data[2:]
                score_eval = eval_to.free_eval(start_fct, offs, problem_size)
                tmp = eval_to.g_tcheby(w, score_eval, z_star)
            else:
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

    return l
