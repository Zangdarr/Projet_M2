import random


#return randomly n indice in range n
def get_n_indices_of(n, size_l):
    indices = []
    k = 0
    while k < n :
        r = random.SystemRandom().randint(0,size_l-1)
        if(not(r in indices)):
            indices.append(r)
            k += 1

    return indices

#return randomly n element of the list_l
def get_n_elements_of(n, list_l):
    indices = get_n_indices_of(n, len(list_l))

    elements = get_elements_of(indices, list_l)

    return elements

def get_elements_of(indices, list_l):
    elements = [ list_l[indices[i]] for i in range(len(indices))]
    return elements


#return the neighboring_size indice of elements that are the nearest from pos in a list of size size_l
def getNeighborsInclusive(pos, neighboring_size, size_l):
    t = [i for i in range(size_l)]

    #[2,3,4,5,6]
    if(neighboring_size > size_l):
        print("ERROR - neighboring_size too long :", neighboring_size)
        exit()
    elif(neighboring_size == size_l):
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
    elif(pos_right > size_l):
        pos_left += size_l - (pos_right)
        pos_right = size_l

    
    return t[pos_left : pos_right]
