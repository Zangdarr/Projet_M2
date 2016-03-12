import version5_reals_prediction as v5
import sys


problem_size               = 10
training_neighborhood_size = 21
nb_samples                 = 10
strategy                   = 'all'
filter_strat               = 'average'
problem = "UF1"
algo_name = "NuSVR_freeeval"


#nb_iterations = problem_size*50
nb_iterations = 40

v5.runOneTime(algo_name, problem, problem_size, nb_samples, nb_iterations, training_neighborhood_size, strategy, filter_strat)
