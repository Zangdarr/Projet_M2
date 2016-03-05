def printObjectives(file_to_write, eval_number,iteration_number,  objectives_table, problem_size, print_every=-1):
    modulo = problem_size
    if(print_every != -1):
        modulo = print_every
    if(iteration_number % modulo == 0):
        tab = [''," ", '', " ", '', " ", '', "\n"]
        for objectives in objectives_table:
            tab[0] = str(iteration_number)
            tab[2] = str(eval_number)
            tab[4] = str(objectives[0])
            tab[6] = str(objectives[1])


            file_to_write.write(''.join(tab))
            #print(iteration_number, eval_number, objectives[0], objectives[1])

def printR2(file_to_write, eval_number, iteration_number,  R2, scores_cv, problem_size, print_every=-1):
    modulo = problem_size
    if(print_every != -1):
        modulo = print_every
    if(iteration_number % modulo == 0):
            tab = [''," ", '', " ", '', " ", '', "\n"]
            tab[0] = str(iteration_number)
            tab[2] = str(eval_number)
            tab[4] = str(round(R2,5))
            tab[6] = str(round(scores_cv, 5))

            file_to_write.write(''.join(tab))
