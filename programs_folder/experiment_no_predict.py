import version4_tcheby_real as v4
import sys


#problem_size=[5,10, 30]
problem_sizes               = [10]
k = 20
training_neighborhood_sizes = [21]

#problem_sizes = [5,10, 30]
#k = 30

#TODO sauvegarder les R² à chaques générations
#TODO faire un autre programme avec 2 modèles, 1 pour f1 et l'autre pour f2. Les données utilisées pour l'apprentissage sont la population courante.S Une version plus avancée serait de prendre pour chaque direction les k dernières solutions qui ont minimisé la directions.


for problem_size in problem_sizes:

    nb_iterations = problem_size*50

    for run in range(k):

        filename = "UF4_MOEAD_PS-" + str(problem_size) + "_R-"+ str(run) +".txt"
        file_to_write = open(filename, 'a')
        v4.experimentWith(file_to_write ,problem_size, nb_iterations, 1)
        file_to_write.close()
        print(filename, "done.")
