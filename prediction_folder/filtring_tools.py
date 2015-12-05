import numpy as np

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



def getInputData(f_neighbors, model_directions, offspring):
    l= []
    id_l = -1
    for i in f_neighbors:
        id_l += 1
        l.append([])

        l[id_l].extend(model_directions[i].tolist()[0])

        l[id_l].extend(offspring)

    return l
