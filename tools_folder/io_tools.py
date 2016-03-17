def printObjectives(file_to_write, eval_number,iteration_number,  objectives_table, problem_size, nb_objectives, print_every=-1):
    modulo = problem_size
    if(print_every != -1):
        modulo = print_every
    if(iteration_number % modulo == 0):
        tab = [" " for i in range(0, 4+2*nb_objectives)]
        tab[-1] = "\n"
        tab = [''," ", '', " ", '', " ", '', "\n"]
        for objectives in objectives_table:
            tab[0] = str(iteration_number)
            tab[2] = str(eval_number)
            for o in range(nb_objectives):
                tab[4+2*o] = str(objectives[o])


            file_to_write.write(''.join(tab))
            #print(iteration_number, eval_number, objectives[0], objectives[1])

def printR2(file_to_write, eval_number, iteration_number,  R2, R2_cv, MSE_cv, MAE_cv, problem_size, print_every=-1):
    modulo = problem_size
    if(print_every != -1):
        modulo = print_every
    if(iteration_number % modulo == 0):
            tab = [''," ", '', " ", '', " ", '', " ", '', " ", '', "\n"]
            tab[0] = str(iteration_number)
            tab[2] = str(eval_number)
            tab[4] = str(round(R2,5))
            tab[6] = str(round(R2_cv, 5))
            tab[8] = str(round(MSE_cv, 5))
            tab[10] = str(round(MAE_cv, 5))

            file_to_write.write(''.join(tab))
