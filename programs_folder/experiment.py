import version5_reals_prediction as v5
import sys


#problem_size=[5,10, 30]
problem_sizes               = [10, 30]
k = 20
training_neighborhood_sizes = [21]

#problem_sizes = [5,10, 30]
#k = 30
nb_sampless                 = [2, 4, 8, 16]
strategies                  = ['single']
filter_strats = ["average", "maxdiff"]
free_eval = [False, True]

UF_name = "UF1"
algo_name = "_MOEAD_ML_NuSVR"

param_print_every = 1


nb_iterations = 40

for run in range(k):

    for filter_strat in filter_strats:

        for problem_size in problem_sizes:
            #nb_iterations = problem_size*50

            for nb_samples in nb_sampless:

              for fe in free_eval:

                for strategy in strategies:
                     if(strategy == 'neighbors'):
                        for training_neighborhood_size in training_neighborhood_sizes:
                            filename = UF_name + algo_name +"_PS-" + str(problem_size) + "_S-" + strategy + "_L-" + str(nb_samples) + "_TS-"+ str(training_neighborhood_size) + "_FS-" + filter_strat + "_FE-" + str(fe) + "_R-"+ str(run) +".txt"
                            filenameR2 = "R2_" + filename
                            file_to_write = open(filename, 'a')
                            file_to_writeR2 = open(filenameR2, 'a')
                            v5.experimentWith(file_to_write ,problem_size, nb_samples, nb_iterations, training_neighborhood_size, strategy, filter_strat, fe, param_print_every, file_to_writeR2)
                            file_to_write.close()
                            file_to_writeR2.close()
                            print(filename, "done.")
                     else:
                            filename = UF_name + algo_name +"_PS-" + str(problem_size) + "_S-" + strategy + "_L-" + str(nb_samples) + "_TS--1" + "_FS-" + filter_strat + "_FE-" + str(fe) +"_R-"+ str(run) +".txt"
                            filenameR2 = "R2_" + filename
                            file_to_write = open(filename, 'a')
                            file_to_writeR2 = open(filenameR2, 'a')

                            v5.experimentWith(file_to_write, problem_size, nb_samples, nb_iterations, -1, strategy, filter_strat, fe, param_print_every, file_to_writeR2)
                            file_to_write.close()
                            file_to_writeR2.close()
                            print(filename, "done.")
