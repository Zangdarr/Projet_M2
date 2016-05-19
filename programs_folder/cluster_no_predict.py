import sys
import version4_tcheby_real as v4
import random


args = sys.argv
_, problem, problem_size, run, nb_iterations, param_print_every, result_folder = args

random.seed(run)

filename = result_folder + "/" + problem + "_MOEAD_PS-" + problem_size + "_R-"+ run +".txt"
file_to_write = open(filename, 'a')
v4.experimentWith(problem, file_to_write ,int(problem_size), int(nb_iterations), int(param_print_every))
file_to_write.close()
#print(filename, "done.")
