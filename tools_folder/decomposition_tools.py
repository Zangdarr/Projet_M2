#-----------------------------------------------------------------------------------------------------------------------------------------------#
#generate the ratio that will be used on both base functions for the N "new" functions, return a table [2][N + 2]
def genRatio_fctbase2(N, check=False):

    numerateur_f1 = [i for i in range(1,N+1)]
    numerateur_f1.insert(0,0)#fct_start1
    numerateur_f1.append(1)  #fct_start2
    numerateur_f2 = numerateur_f1.copy()
    numerateur_f2.reverse()

    denominateur = [N+1 for i in range(1,N+1)]
    denominateur.insert(0,1)#fct_start1
    denominateur.append(1)  #fct_start2

    if(check):
      print("## genRatio_fctbase2 : \nnumerateur f1 :", numerateur_f1, "\nnumerateur_f2 :", numerateur_f2 ,"\ndenominateur :", denominateur)

    return (numerateur_f1, numerateur_f2, denominateur)
