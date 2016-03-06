import copy

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

def getDirections(nb_functions, nb_objectives):
    if(nb_objectives == 2):
        return genRatio_fctbase2(nb_functions)
    elif(nb_objectives == 3):
        print("Decomposition for 3 objectives not yet implemented")
        exit()
    else:
        print("Not 2 or 3 objectives : ERROR")
        exit()


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
