"""
def getDecisionSpace(filename, check=False):
   l = []
   with open(filename, 'r') as f :
        for line in f :
           linewithoutreturnline = line[:-1]
           l.append(linewithoutreturnline)

   if(check):
     print("getDecisionSpace return list : \n" ,l)

   return l
"""
#Retourne l'espace objectif selon les fonctions de base et l'espace de decision/
def getObjectiveSpace(start_fct, decision_space, check=False):
     l = [[] for i in range(len(start_fct))]
     for token in decision_space:

        for i in range(len(start_fct)):
            l[i].append((start_fct[i])(token))

     if(check):
       print("# getObjectiveSpace return list :\n", l)

     return l
