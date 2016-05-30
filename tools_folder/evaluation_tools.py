#--------------------------------------------------------------------------------------------------------------
#EVALUATION

epsilon = 10**(-3)
z_star = []
z_star_decal = []

def initZstar(initial_z_star):
    global z_star, z_star_decal, epsilon
    z_star = initial_z_star
    z_star_decal = []
    for z in z_star:
        z_star_decal.append( z - epsilon )


def getZstar():
    global z_star
    return z_star

def getZstar_with_decal():
    global z_star_decal
    return z_star_decal


def min_update_Z_star(new_scores, nb_objectives):
    global z_star
    new_z_star = []
    has_changed_bool = False
    for i in range(nb_objectives):
        if(z_star[i] > new_scores[i]):
            new_z_star.append(new_scores[i])
            has_changed_bool = True
        else:
            new_z_star.append(z_star[i])

    if(has_changed_bool):
        initZstar(new_z_star)

    return has_changed_bool

#evaluate the distance of a solution from the z-optimal solution
def g_tcheby(dir, score, opt_scores):
    #return max(dir[0]*abs(score[0]-opt_scores[0]),dir[1]*abs(score[1]-opt_scores[1]))
    mmax = 0.0
    i = 0
    for sc in score:
        tmp = dir[i]*abs(sc -opt_scores[i])
        if(mmax < tmp):
            mmax = tmp
        i += 1
    return mmax

def getManyTcheby(training_inputs, training_scores, z_star, training_set_size):
    tab_tcheby = []
    for i in range(training_set_size):
        tmp = g_tcheby(training_inputs[i][:3], training_scores[i], z_star )
        tab_tcheby.append(tmp)
    return tab_tcheby

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
