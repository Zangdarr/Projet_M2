import numpy as np
import sys
sys.path.insert(0,"../tools_folder/")
import generics_tools as gen
import evaluation_tools as eval_to


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
    tmp1, tmp2 = directions

    tmp1 = np.transpose(np.matrix(tmp1))
    tmp2 = np.transpose(np.matrix(tmp2))
    result = np.hstack((tmp1, tmp2))

    return result

def getTrainingSet(training_directions, training_individuals, individuals_objectives ,z_star, strategy, population_size, training_neighborhood_size):
    if(strategy == 'all'):
        return getTrainingSetAll(training_directions, training_individuals, individuals_objectives, z_star)
    elif(strategy == 'single'):
        return getTrainingSetSingle(training_directions, training_individuals, individuals_objectives, z_star)
    elif(strategy == 'neighbors'):
        return getTrainingSetNeighbors(training_directions, training_individuals, individuals_objectives, z_star, population_size, training_neighborhood_size)


def getTrainingSetNeighbors(training_directions, training_individuals, individuals_objectives, z_star, population_size, training_neighborhood_size):
    individual_id    = -1
    training_inputs  = []
    training_outputs = []

    for individual in training_individuals:
        individual_id += 1

        if(individual in training_individuals[0:individual_id]):
            continue

        neighbors_directions = getTrainingNeighborsInclusive(individual_id, training_neighborhood_size, population_size)

        for direction in neighbors_directions:
            current_dir = training_directions[direction].tolist()[0]
            training_input = []
            training_input.extend(current_dir)
            training_input.extend(individual)

            training_output = eval_to.g_tcheby(current_dir, individuals_objectives[individual_id], z_star)

            training_inputs.append(training_input)
            training_outputs.append(training_output)
    return training_inputs, training_outputs


def getTrainingSetSingle(training_directions, training_individuals, individuals_objectives, z_star):
    individual_id    = -1
    training_inputs  = []
    training_outputs = []

    for individual in training_individuals:
        individual_id += 1

        if(individual in training_individuals[0:individual_id]):
            continue

        direction = training_directions[individual_id%100]
        current_dir = direction.tolist()[0]
        training_input = []
        training_input.extend(current_dir)
        training_input.extend(individual)

        training_output = eval_to.g_tcheby(current_dir, individuals_objectives[individual_id], z_star)

        training_inputs.append(training_input)
        training_outputs.append(training_output)

    return training_inputs, training_outputs


def getTrainingSetAll(training_directions, training_individuals, individuals_objectives, z_star):
    individual_id    = -1
    training_inputs  = []
    training_outputs = []

    for individual in training_individuals:
        individual_id += 1

        if(individual in training_individuals[0:individual_id]):
            continue

        for direction in training_directions:
            current_dir = direction.tolist()[0]
            training_input = []
            training_input.extend(current_dir)
            training_input.extend(individual)

            training_output = eval_to.g_tcheby(current_dir, individuals_objectives[individual_id], z_star)

            training_inputs.append(training_input)
            training_outputs.append(training_output)
    return training_inputs, training_outputs


#training_individuals = [[0.30089509527814207, 0.2750430971678284, 0.11123324286837022, -0.3807695490236809], [0.21539370137187852, -0.30021739669398095, 0.6487370145784062, 0.05144409142146977], [0.013626558414417733, 0.7731835891593353, -0.3353098201174083, -0.16848424096831227], [0.4542618766183695, 0.29083190434551365, 0.13043503555443925, 0.7002786006279191], [0.08055754438034246, -0.9336312350209366, 0.44682488645829044, 0.3699833042385907], [0.6077900301708405, 0.058803316649457704, -0.9013354310430177, 0.25651977948424287], [0.43303947778238827, -0.4385169761434644, -0.423142428691333, -0.014377766653171697]]
#training_directions  = [[1,2,3,4,5,6,7],[1,2,3,4,5,6,7]]
