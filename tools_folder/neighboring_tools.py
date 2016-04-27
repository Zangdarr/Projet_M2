import random


#return the neighboring_size indice of elements that are the nearest from pos in a list of size size_l
def getNeighborsInclusive(pos, neighboring_size, size_l, delta=0):
    t = [i for i in range(size_l)]

    #proba to give all functions as neighbourhood
    rnd = random.SystemRandom().random()
    if( not(rnd < delta)):
       return t, size_l

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

    return t[pos_left : pos_right], neighboring_size
