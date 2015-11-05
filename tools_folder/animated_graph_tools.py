import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from decomposition_tools import genRatio_fctbase2

title = "Default title"
axe_x_name = "Default x axe"
axe_y_name = "Default y axe"

def update(data):
    plt.clf()
    plt.title(title)
    plt.xlabel(axe_x_name)
    plt.ylabel(axe_y_name)
    datax1y1, datax2y2, tic, evals, max_f1, max_f2 = data

    x,y = datax1y1
    #plt.scatter(x, y,  color='blue', label="Objective space")
    x1,y1 = np.transpose(datax2y2)
    plt.scatter(x1, y1, color='red', label="functions's best solutions" )
    nb_functions = len(datax2y2)


    ratio = genRatio_fctbase2(nb_functions - 2)# -2 a cause des deux fonctions de base
    ratio_num_x = ratio[0]
    ratio_num_y = ratio[1]
    ratio_denum = ratio[2]


    mm = max(max_f1, max_f2)+ 10

    zeros = np.array([0 for i in range(mm)])
    array = np.array([i for i in range(mm)])
    plt.plot(array,zeros, color='green')
    plt.plot(zeros, array, color = 'green')
    """
    for i in range(len(ratio_num_x)):
       line_x = np.dot(array[0:mm*2//len(ratio_num_x)], ratio_num_x[i])
       line_y = np.dot(array[0:mm*2//len(ratio_num_x)], ratio_num_y[i])
       plt.plot(line_x, line_y, color='green')
    """
    plt.legend()
    txt = []
    txt.append("iter ")
    txt.append(str(tic))
    txt.append("\n")
    txt.append(str(nb_functions))
    txt.append(" functions\n")
    txt.append("Nb Evaluations : ")
    txt.append(str(evals))
    plt.text(5, 5, ''.join(txt))
    plt.scatter(max_f1, max_f2, color="yellow")
    plt.plot([i for i in range(max_f1)], [max_f2 for i in range(max_f1)],color="yellow")
    plt.plot([max_f1 for i in range(max_f2)], [i for i in range(max_f2)],color="yellow")

    return 1


def runAnimatedGraph(fct, titre, name_x, name_y, sleep=10):
    global title, axe_x_name, axe_y_name
    title = titre
    axe_x_name = name_x
    axe_y_name = name_y
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig ,update, fct, blit=False, interval=sleep,
    repeat=False)
    plt.show()
