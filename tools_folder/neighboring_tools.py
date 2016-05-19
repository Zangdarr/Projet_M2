import random


neighboring_tab  = []
full_neighbors   = []
neighboring_size = -1
directions_nb    = -1

#Initialize the neighboring tables and other glabal variables
def initNeighboringTab(nb_directions, nghb_size, weights, nb_objectives):
    global neighboring_tab, full_neighbors, neighboring_size, directions_nb

    directions_nb    = nb_directions
    neighboring_size = nghb_size
    full_neighbors = [i for i in range(directions_nb)]

    distances_tabs = [[computeDistance(i,j,weights, nb_objectives) for j in range(nb_directions)] for i in range(nb_directions)]

    for i in range(nb_directions):
        tmp_sorted_tab = sorted(range(nb_directions), key=lambda k: distances_tabs[i][k])

        neighboring_tab.append(tmp_sorted_tab[0:neighboring_size])

def computeDistance(posA, posB, weights, nb_objectives):
    distance = 0.0
    for i in range(nb_objectives):
        distance += abs(weights[i][posA] - weights[i][posB])
    return distance

#return the neighboring of the direction in pos or the complete index table following the probality deltaN
def getNeighborsOf(pos, deltaN):
    global neighboring_tab, full_neighbors, neighboring_size, directions_nb

    rnd = random.random()
    if( not(rnd < deltaN)):
       return full_neighbors, directions_nb

    return neighboring_tab[pos], neighboring_size


"""
def initNeighboringTab(nb_directions, nghb_size):
    global neighboring_tab, full_neighbors, neighboring_size, directions_nb

    directions_nb    = nb_directions
    neighboring_size = nghb_size
    full_neighbors = [i for i in range(directions_nb)]

    for pos in range(0, nb_directions):
        neighboring_tab.append(getNeighborsInclusive(pos, neighboring_size))


#return the neighboring_size indice of elements that are the nearest from pos in a list of size directions_nb
def getNeighborsInclusive(pos, neighboring_size):
    global directions_nb

    t = [i for i in range(directions_nb)]

    #[2,3,4,5,6]
    if(neighboring_size > directions_nb):
        print("ERROR - neighboring_size too long :", neighboring_size)
        exit()
    elif(neighboring_size == directions_nb):
        return t

    elif(neighboring_size == 0):
        print("ERROR - neighboring_size == 0" )
        exit()

    reverse_parite = (neighboring_size+1) %2

    left_size = neighboring_size // 2
    right_size = left_size - reverse_parite

    pos_left = pos - left_size
    pos_right = pos + right_size + 1

    if(pos_left < 0):
        pos_right += pos_left * -1
        pos_left = 0
    elif(pos_right > directions_nb):
        pos_left += directions_nb - (pos_right)
        pos_right = directions_nb

    return t[pos_left : pos_right]
"""
