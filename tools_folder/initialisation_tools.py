#-------------------------------------------------------------------------------
#INITIALISATION

#Randomly initialise the best solution for each functions generated
def initRandom(generation_fct, nb_functions, problem_size, search_space):
    tab = []
    for i in range(nb_functions):
        tmp = generation_fct(problem_size, search_space)
        tab.append(tmp)
    return tab
