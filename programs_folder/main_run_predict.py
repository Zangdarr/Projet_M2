import version5_reals_prediction as v5
import sys


problem_size               = 10          # 10 30
training_neighborhood_size = 21          # 21
nb_samples                 = 10          # 2 4 8 16
strategy                   = 'all'       # single all
filter_strat               = 'numberdir' # AvScl best by_direction numberdir
problem = "UF1"                          # UF1 UF2 UF3 UF4 UF5 UF6 UF7 UF8 UF9 UF10
algo_name = "NuSVR-pop"                  # NuSVR-freeeval NuSVR-pop NuSVR-popnewest NuSVR-newest NuSVR-fulleval


#nb_iterations = problem_size*50
nb_iterations = 40

# launch the real-time graphical version of the algorithm with the above parameters
v5.runOneTime(algo_name, problem, problem_size, nb_samples, nb_iterations, training_neighborhood_size, strategy, filter_strat)
