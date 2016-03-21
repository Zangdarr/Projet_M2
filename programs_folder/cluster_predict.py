import sys
import version5_reals_prediction as v5

args = sys.argv

_, problem, algo_name, problem_size, strategy, nb_samples, filter_strat, run, nb_iterations, param_print_every, result_folder = args

if("freeeval" in algo_name):
    filename = result_folder + "/" + problem + "_" + algo_name +"_PS-" + str(problem_size) + "_S-none" + "_L-" + str(nb_samples) + "_TS--1" + "_FS-" + filter_strat +"_R-"+ str(run) +".txt"
    filenameR2 = result_folder + "/" + "R2_" + problem + "_" + algo_name +"_PS-" + str(problem_size) + "_S-none" + "_L-" + str(nb_samples) + "_TS--1" + "_FS-" + filter_strat + "_R-"+ str(run) +".txt"
else:
    tmpp = problem + "_" + algo_name +"_PS-" + str(problem_size) + "_S-" + strategy + "_L-" + str(nb_samples) + "_TS--1" + "_FS-" + filter_strat +"_R-"+ str(run) +".txt"    
    filename      = result_folder + "/" +  tmpp
    filenameR2    = result_folder + "/" + "R2_" + tmpp
    filenameDIR   = result_folder + "/" + "DIR_" + tmpp
    filenameSCORE = result_folder + "/" + "SCORE_" + tmpp

file_to_write = open(filename, 'a')
file_to_writeR2 = open(filenameR2, 'a')
v5.experimentWith(algo_name, problem, file_to_write, int(problem_size), int(nb_samples), int(nb_iterations), -1, strategy, filter_strat, int(param_print_every), file_to_writeR2, filenameDIR, filenameSCORE)
file_to_write.close()
file_to_writeR2.close()
#print(filename, "done.")
