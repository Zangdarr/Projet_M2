#--------------------------------------------------------------------------------------------------------------
#EVALUATION

#evaluate the distance of a solution from the z-optimal solution
def g_tcheby(dir, score, opt_scores):
    return max(dir[0]*abs(score[0]-opt_scores[0]),dir[1]*abs(score[1]-opt_scores[1]))

#evaluation of an offspring with the 2 base functions
nb_evals = 0
def eval(start_fct, problem, problem_size):
    global nb_evals
    nb_evals += 1
    problem_scores = [start_fct[f](problem, problem_size) for f in range(len(start_fct))]
    return problem_scores, nb_evals

def free_eval(start_fct, problem, problem_size):
    problem_scores = [start_fct[f](problem, problem_size) for f in range(len(start_fct))]
    return problem_scores
