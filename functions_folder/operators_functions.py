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
    r = random.SystemRandom().random()
    if(r < 1 - CR):
        return x_r1
    mix = []
    if(vector_size < 500):
        for i in range(vector_size):
            tmp = x_r1[i] + F * (x_r2[i] - x_r3[i])
            mix.append(tmp)
    else:
       array_1 = np.array(x_r1)
       array_2 = np.array(x_r2)
       array_3 = np.array(x_r3)

       tmp = array_1 + F * (array_2 - array_3)
       mix = list(tmp)
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

def sigmak(vector_size, distrib_index_n):
    rand = random.SystemRandom().random()
    tab = []
    if(rand < 0.5):
       for i in range(vector_size):
           tmp = (2*rand)**(1/(distrib_index_n+1)) -1
           tab.append(tmp)
    else:
       for i in range(vector_size):
           tmp = 1 - (2-2*rand)**(1/(distrib_index_n+1))
           tab.append(tmp)
    return tab

def polynomial_mutation(mix, vector_size, search_space, distrib_index_n, pm):
    r = random.SystemRandom().random()
    if(r < 1 - pm):
        return mix

    bk_ak_tab = bk_ak(search_space)

    sigmak_tab = sigmak(vector_size, distrib_index_n)

    mix_bis = []
    if(vector_size < 500):
        for i in range(vector_size):
            tmp = mix[i] + sigmak_tab[i] * bk_ak_tab[i]
            mix_bis.append(tmp)
    else:
         array_1 = np.array(mix)
         array_2 = np.array(sigmak_tab)
         array_3 = np.array(bk_ak_tab)

         tmp = array_1 + array_2 * array_3
         mix_bis = list(tmp)
    return mix_bis
