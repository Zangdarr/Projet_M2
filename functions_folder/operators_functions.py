import random

########################################################################
# Vector generation functions
########################################################################

def genVector(size, search_space):
    vector = []
    len_search_space = len(search_space)
    for i in range(len_search_space):
       lim_b, lim_h = search_space[i][1]
       for j in range(search_space[i][0]):
         r = random.SystemRandom().uniform(lim_b,lim_h)
         vector.append(r)
    return vector


########################################################################
# Repair offspring function
########################################################################

def repair_offspring(offspring, search_space):
    tmp = []
    search_space_len = len(search_space)
    prev = 0
    for i in range(search_space_len):
        lim_b, lim_h = search_space[i][1]
        tmp_len = search_space[i][0]
        for j in range(tmp_len):
            pos = prev + j
            if(offspring[pos] > lim_h or offspring[pos] < lim_b):
                tmp.append(random.SystemRandom().uniform(lim_b,lim_h))
            else:
                tmp.append(offspring[pos])
        prev = tmp_len
    return tmp


########################################################################
# Crossovers functions
########################################################################

def DE_Operator(x_r1, x_r2, x_r3, F, vector_size, CR):
    mix = []
    for i in range(vector_size):

        r = random.SystemRandom().random()
        if(r < 1 - CR):
            mix.append(x_r1)
        else:
            tmp = x_r1[i] + F * (x_r2[i] - x_r3[i])
            mix.append(tmp)

    return mix


########################################################################
# Mutations functions
########################################################################

def bk_ak(search_space):
    tmp = []
    search_space_len = len(search_space)
    for i in range(search_space_len):
        lim_b, lim_h = search_space[i][1]
        for j in range(search_space[i][0]):
            tmp.append(lim_h - lim_b)
    return tmp

def sigmak(distrib_index_n):
    rand = random.SystemRandom().random()

    if(rand < 0.5):
       tmp = (2*rand)**(1/(distrib_index_n+1)) -1
    else:
       tmp = 1 - (2-2*rand)**(1/(distrib_index_n+1))

    return tmp

def polynomial_mutation(mix, vector_size, search_space, distrib_index_n, pm):
    mix_bis = []
    bk_ak_tab = bk_ak(search_space)

    for i in range(vector_size):
        r = random.SystemRandom().random()
        if(r < 1 - pm):
            mix_bis.append(mix[i])
        else:
            sigma = sigmak(distrib_index_n)
            tmp = mix[i] + sigma * bk_ak_tab[i]
            mix_bis.append(tmp)

    return mix_bis
