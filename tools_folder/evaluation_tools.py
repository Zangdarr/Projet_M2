#--------------------------------------------------------------------------------------------------------------
#EVALUATION

def min_update_Z_star(z_star, new_scores, nb_objectives):
    new_z_star = []
    has_changed_bool = False
    for i in range(nb_objectives):
        if(z_star[i] > new_scores[i]):
            new_z_star.append(new_scores[i])
            has_changed_bool = True
        else:
            new_z_star.append(z_star[i])

    return new_z_star, has_changed_bool

#evaluate the distance of a solution from the z-optimal solution
def g_tcheby(dir, score, opt_scores):
    return max(dir[0]*abs(score[0]-opt_scores[0]),dir[1]*abs(score[1]-opt_scores[1]))

#evaluation of an offspring with the 2 base functions
nb_evals = 0
def eval(start_fct, problem, problem_size):
    global nb_evals
    nb_evals += 1
    problem_scores = [start_fct[f](problem, problem_size) for f in range(len(start_fct))]
    return problem_scores

def free_eval(start_fct, problem, problem_size):
    problem_scores = [start_fct[f](problem, problem_size) for f in range(len(start_fct))]
    return problem_scores

def getNbEvals():
    global nb_evals
    return nb_evals

def resetEval():
    global nb_evals
    nb_evals = 0
