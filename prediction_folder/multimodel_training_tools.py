import numpy as np
import generics_tools as gen
import evaluation_tools as eval_to


#####Main

def getTrainingSet(solution_list, solution_objectives):
    training_inputs = np.array(solution_list)
    training_outputslist = np.array(solution_objectives).T
    return training_inputs, training_outputslist, training_inputs.size

def multimodel_fit(model_tab, training_inputs, training_outputslist):
    current_i = 0
    for model in model_tab:
        model.fit(training_inputs, training_outputslist[current_i])
        current_i += 1

#####Secondary

def getTrainingNeighborsInclusive(pos, neighboring_size, size_l):
    t = [i for i in range(size_l)]
    reverse_parite = (neighboring_size+1) %2

    left_size = neighboring_size // 2
    right_size = left_size - reverse_parite

    pos_left = pos - left_size
    pos_right = pos + right_size + 1

    if(pos_left < 0):
        pos_right += pos_left * -1
        pos_left = 0
    elif(pos_right > size_l):
        pos_left += size_l - (pos_right)
        pos_right = size_l
    #print(pos_left, pos_right, neighboring_size)
    return t[pos_left : pos_right], neighboring_size

def getDirectionsTrainingMatrix(directions):
    tmmp = np.matrix(directions)
    result = tmmp.T

    return result
