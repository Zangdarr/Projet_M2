import generics_tools as gt


def extended_sampling(f,f_neighbors, sampling_param, nb_samples):
    l = []
    for i in range(nb_samples):
        l.append(sampling(f,f_neighbors, sampling_param))
    return l


def sampling(f, f_neighbors, sampling_param):
    crossover_fct, mutation_fct, repair_fct, best_decisions, F, problem_size, CR, search_space, distrib_index_n, pm = sampling_param
    #select two indice of function in the neighbors + f
    l, k = gt.get_n_elements_of(2, f_neighbors)
    #application of a crossing operator with the current best solution and 2 others from the neighbourhood l & k
    r1, r2, r3 = f, l, k
    mix = crossover_fct(best_decisions[r1],best_decisions[r2],best_decisions[r3], F, problem_size, CR)
    #application of a a bit flip on the newly made solution
    mix_bis = mutation_fct(mix, problem_size, search_space, distrib_index_n, pm)
    #repair step : search space
    mix_ter = repair_fct(mix_bis, search_space)

    return mix_ter
