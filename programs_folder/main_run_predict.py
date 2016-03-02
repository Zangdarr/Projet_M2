import version5_reals_prediction as v5
import sys


problem_size               = 10
training_neighborhood_size = 21
nb_samples                 = 10
strategy                   = 'all'
filter_strat               = 'average'
free_eval                  = False

#TODO sauvegarder les R² à chaques générations
#TODO faire un autre programme avec 2 modèles, 1 pour f1 et l'autre pour f2. Les données utilisées pour l'apprentissage sont la population courante.S Une version plus avancée serait de prendre pour chaque direction les k dernières solutions qui ont minimisé la directions.


#nb_iterations = problem_size*50
nb_iterations = 40

v5.runOneTime(problem_size, nb_samples, nb_iterations, training_neighborhood_size, strategy, filter_strat, free_eval)
