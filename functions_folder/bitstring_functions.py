import random

#return number of '1' in a binary string
def f1(bin_str):
   cpt_1 = 0
   for i in range(len(bin_str)):
      if bin_str[i] == 1:
         cpt_1 += 1
   return cpt_1

#return number of '0' in a binary string
def f2(bin_str):
   return len(bin_str) - f1(bin_str)


def genBS(taille):
    bstr = []
    for i in range(taille):
       r = random.SystemRandom().randint(0,1)
       if(r):
           bstr.append(1)
       else:
           bstr.append(0)
    return bstr

def mixOperator(l, k, p):
    r = random.SystemRandom().randint(1,len(l)-1)
    if(r>p):
        return l
    r = random.SystemRandom().randint(1,len(l)-1)
    o = random.SystemRandom().randint(0,1)
    if(o):
        mix = l[0:r] + k[r:]
    else:
        mix = k[0:r] + l[r:]

    return mix


def onebitflip(bitstring, f):

    l_bs = bitstring.copy()
    l = len(bitstring)
    r = random.SystemRandom().randint(0,l-1)

    l_bs[r] = 0 if l_bs[r] == 1 else 1

    return l_bs

def bitflip(bitstring, f, flip=1):
    #TODO passé la longueur en param
    #proba de flip pour 1 bit donne
    bs_len = len(bitstring)
    prob_flip = flip / bs_len
    l_bs = bitstring.copy()

    for i in range(bs_len):
        r = random.SystemRandom().random()
        if(r < prob_flip):
            l_bs[i] = 0 if l_bs[i] == 1 else 1

    return l_bs

#return false optimals scores that could not be reach by any bitstring of a certain size with the starting function
def get_Z_optimal(nb_start_fct, bitstring_size):
    #TODO la position du z optimal dépend des best f1 et f2 actuel

    #this is the score for a string with two time more of caractere with half 0 and 1
    scores_tab = [bitstring_size for i in range(nb_start_fct)]
    return scores_tab
