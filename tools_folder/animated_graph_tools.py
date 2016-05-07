import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import math

title = "Default title"
axe_x_name = "Default x axe"
axe_y_name = "Default y axe"

def update(data):
    global tf
    #clean graph
    plt.clf()
    #globals informations
    plt.title(title)
    plt.xlabel(axe_x_name)
    plt.ylabel(axe_y_name)
    plt.xlim([0,1.2])
    plt.ylim([0,1.2])
    #recuparation data separetly
    datax1y1, datax2y2, tic, evals, z_star, pop_size, isReals = data

    max_f1, max_f2 = z_star
    #archive
    x,y = datax1y1
    plt.scatter(x, y,  color='blue', label="archive", marker="x")
    #best decision representation in objective space of the n functions
    x1,y1 = np.transpose(datax2y2)
    plt.scatter(x1, y1, color='red', label="approx front pareto", marker="d")
    nb_functions = len(datax2y2)

    #draw axis
    mm = 0
    text_pos_x = 0
    text_pos_y = 0
    if(isReals):
       max_f1 = int(max_f1)+1
       max_f2 = int(max_f2)+1
       mm = max(max_f1, max_f2)+ 1
       if(len(tf) == 2):
           plt.scatter(tf[0], tf[1], s=0.5, color="purple", alpha=0.5, label="front pareto")
       text_pos_x = 1
       text_pos_y = 1
    else:
       mm = max(max_f1, max_f2)+ 10
       text_pos_x = 5
       text_pos_y = 5

    zeros = np.array([0 for i in range(mm)])
    array = np.array([i for i in range(mm)])
    plt.plot(array,zeros, color='green')
    plt.plot(zeros, array, color = 'green')

    #informative text
    txt = []
    txt.append("population size ")
    txt.append(str(pop_size))
    txt.append("\niter ")
    txt.append(str(tic))
    txt.append("\n")
    txt.append(str(nb_functions))
    txt.append(" functions\n")
    txt.append("nb evaluations : ")
    txt.append(str(evals))
    plt.text(text_pos_x, text_pos_y, ''.join(txt))

    #draw z-optimal point and limit line
    if(not(isReals)):
        plt.scatter(max_f1, max_f2, color="yellow")
        plt.plot([i for i in range(max_f1)], [max_f2 for i in range(max_f1)],color="yellow")
        plt.plot([max_f1 for i in range(max_f2)], [i for i in range(max_f2)],color="yellow")

    #draw legend of the graph
    plt.legend()
    return 1

tf = []
def runAnimatedGraph(fct, end_fct, pareto_front_fct, titre, name_x, name_y, sleep=10):
    global title, axe_x_name, axe_y_name, tf
    if(pareto_front_fct != -1):
        tf = pareto_front_fct()
    title = titre
    axe_x_name = name_x
    axe_y_name = name_y
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig ,update, fct, blit=False, interval=sleep,
    repeat=False)
    plt.show()
    return end_fct()
