import version5_reals_prediction as v5
import sys


#problem_size=[5,10, 30]
problem_sizes               = [10]
k = 20
training_neighborhood_sizes = [21]

#problem_sizes = [5,10, 30]
#k = 30
nb_sampless                 = [16]
strategies                  = ['all']


#TODO sauvegarder les R² à chaques générations
#TODO faire un autre programme avec 2 modèles, 1 pour f1 et l'autre pour f2. Les données utilisées pour l'apprentissage sont la population courante.S Une version plus avancée serait de prendre pour chaque direction les k dernières solutions qui ont minimisé la directions.


for run in range(k):

    for problem_size in problem_sizes:
        nb_iterations = problem_size*50

        for nb_samples in nb_sampless:

            for strategy in strategies:
                 if(strategy == 'neighbors'):
                    for training_neighborhood_size in training_neighborhood_sizes:
                        filename = "UF4_MOEAD_ML_PS-" + str(problem_size) + "_S-" + strategy + "_L-" + str(nb_samples) + "_TS-"+ str(training_neighborhood_size)+ "_R-"+ str(run) +".txt"
                        file_to_write = open(filename, 'a')
                        v5.experimentWith(file_to_write ,problem_size, nb_samples, nb_iterations, training_neighborhood_size, strategy, filter_strat, free_eval)
                        file_to_write.close()
                        print(filename, "done.")
                 else:
                        filename = "UF4_MOEAD_ML_PS-" + str(problem_size) + "_S-" + strategy + "_L-" + str(nb_samples) + "_TS--1_R-"+ str(run) +".txt"
                        file_to_write = open(filename, 'a')
                        v5.experimentWith(file_to_write, problem_size, nb_samples, nb_iterations, -1, strategy, filter_strat, free_eval)
                        file_to_write.close()
                        print(filename, "done.")
