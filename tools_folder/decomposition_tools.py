import copy

WEIGHT2D_FILE = "../tools_folder/SLD-2objs-100wei.ws"
WEIGHT3D_FILE = "../tools_folder/SLD-3objs-210wei.ws"
#-----------------------------------------------------------------------------------------------------------------------------------------------#
"""
#generate the ratio that will be used on both base functions for the N "new" functions, return a table [2][N + 2]
def genRatio_fctbase2(N, check=False):

    numerateur_f1 = [i for i in range(1,N+1)]
    numerateur_f1.insert(0,0)#fct_start1
    numerateur_f1.append(1)  #fct_start2
    numerateur_f2 = numerateur_f1.copy()
    numerateur_f2.reverse()

    denominateur = [N+1 for i in range(1,N+1)]
    denominateur.insert(0,1)#fct_start1
    denominateur.append(0)  #fct_start2

    if(check):
      print("## genRatio_fctbase2 : \nnumerateur f1 :", numerateur_f1, "\nnumerateur_f2 :", numerateur_f2 ,"\ndenominateur :", denominateur)

    return (numerateur_f1, numerateur_f2, denominateur)
"""

def getDirections(nb_directions, nb_objectives):
    if(nb_objectives == 2 and nb_directions == 100):
        return getWeightDecompositionFromFile(nb_directions, nb_objectives, WEIGHT2D_FILE)
    elif(nb_objectives == 3 and nb_directions == 210):
        return getWeightDecompositionFromFile(nb_directions, nb_objectives, WEIGHT3D_FILE)
    else:
        print("Error in configuration : 2obj and 100 dir or 3obj and 210 dir")
        exit()

def getWeightDecompositionFromFile(nb_directions, nb_objectives, filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    weights = [[] for i in range(nb_objectives)]
    for line in lines:
        splitted_line = line.split(" ")
        for obj in range(nb_objectives):
            weights[obj].append(float(splitted_line[obj]))

    return weights

"""
#generate the ratio that will be used on the N functions, return 2 table  N size
def genRatio_fctbase2(nb_functions, check=False):

    #ratio for the first starting function
    ratio_tab_f1 = []

    divide_value = float(nb_functions -1)
    ratio_tab_f1.append(0.0)
    for i in range(1, nb_functions):
        ratio_tab_f1.append(i / divide_value)

    #ratio for the second starting function
    ratio_tab_f2 = copy.copy(ratio_tab_f1)
    ratio_tab_f2.reverse()

    return [ratio_tab_f1, ratio_tab_f2]
"""
