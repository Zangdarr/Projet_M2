import version4_tcheby_real as v4
import sys


problem_size               = 30


#TODO sauvegarder les R² à chaques générations
#TODO faire un autre programme avec 2 modèles, 1 pour f1 et l'autre pour f2. Les données utilisées pour l'apprentissage sont la population courante.S Une version plus avancée serait de prendre pour chaque direction les k dernières solutions qui ont minimisé la directions.


nb_iterations = problem_size*50
nb_iterations = 40
v4.runOneTime(problem_size, nb_iterations)
