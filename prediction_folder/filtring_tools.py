import numpy as np

#--------------------------------------------------------------------------------------------------------------
# MODEL-BASED-FILTRING

def model_based_filtring(filter_strat, param):

    if(filter_strat == 'average'):
        model, f_neighbors, list_offspring, model_directions = param
        return average_model_based(model, f_neighbors, list_offspring, model_directions)
    elif(filter_strat == 'free'):
        model, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star = param
        return free_model_based(model, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star)


def average_model_based(model, f_neighbors, list_offspring, model_directions):
    id_offspring = -1
    index_best = -1
    score_best = 0
    for offspring in list_offspring:
        id_offspring += 1
        average_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)
        f_input_data = np.matrix(f_input_data)

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


def free_model_based(model, f_neighbors, list_offspring, model_directions, start_fct, problem_size, z_star):
    id_offspring = -1
    index_best = -1
    score_best = 0
    for offspring in list_offspring:
        id_offspring += 1
        average_score = 0

        f_input_data = getInputData(f_neighbors, model_directions, offspring)

        count = 0
        for data in f_input_data:
            w = data[0:2]
            offs = data[2:]
            score_eval = evals_to.free_eval(start_fct, offs, problem_size)
            score_gtcheby = g_tcheby(w, score_eval, z_star)
            average_score += score_gtcheby
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
