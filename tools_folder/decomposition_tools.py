#-----------------------------------------------------------------------------------------------------------------------------------------------#
"""
NOT USED IN TCHEBY
# generate N balanced new functions from the Nb base functions, return N + Nb functions
def genDecompositionFunction(N_start_fct, N_new_fct, check=True):

   ratio = genRatio_fctbase2(N_new_fct, check=True)

   f1_numerateur = ratio[0]
   f2_numerateur = ratio[1]
   denumerateur  = ratio[2]

   list_new_fct = []

   for i in range(N_new_fct + N_start_fct):
      new_fct = lambda f1, f2, i=i : (f1_numerateur[i]/denumerateur[i]) * f1 + (f2_numerateur[i]/denumerateur[i]) * f2
      list_new_fct.append(new_fct)


   if(check):
     print("# genDecompositionFunction return fct list :\n", list_new_fct)

   return list_new_fct
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
    denominateur.append(1)  #fct_start2

    if(check):
      print("## genRatio_fctbase2 : \nnumerateur f1 :", numerateur_f1, "\nnumerateur_f2 :", numerateur_f2 ,"\ndenominateur :", denominateur)

    return (numerateur_f1, numerateur_f2, denominateur)
