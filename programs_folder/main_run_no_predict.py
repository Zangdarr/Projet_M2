import version4_tcheby_real as v4
import sys


problem_size               = 30


#TODO sauvegarder les R^2 a chaques generations
#TODO faire un autre programme avec 2 modeles, 1 pour f1 et l'autre pour f2. Les donnees utilisees pour l'apprentissage sont la population courante. S Une version plus avancee serait de prendre pour chaque direction les k dernieres solutions qui ont minimise la directions.


nb_iterations = problem_size*50
nb_iterations = 40
problem = "UF1"

v4.runOneTime(problem, problem_size, nb_iterations)
