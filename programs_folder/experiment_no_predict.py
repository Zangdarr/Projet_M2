import version4_tcheby_real as v4
import sys


#problem_size=[5,10, 30]
problem_sizes               = [10, 30]
k = 20
training_neighborhood_sizes = [21]
problems = ["UF1", "UF2", "UF3"]

#problem_sizes = [5,10, 30]
#k = 30


for problem_size in problem_sizes:

    nb_iterations = problem_size*50
    nb_iterations = 40

    for problem in problems:

        for run in range(k):

            filename = problem + "_MOEAD_PS-" + str(problem_size) + "_R-"+ str(run) +".txt"
            file_to_write = open(filename, 'a')
            v4.experimentWith(problem, file_to_write ,problem_size, nb_iterations, 1)
            file_to_write.close()
            print(filename, "done.")
