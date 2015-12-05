archive_sol = []
archive_score = [[],[]]
archive_size = 0

def getArchive():
    return archive_sol

def getArchiveScore():
    return archive_score

def archivePut(solution, score):
    global archive_sol, archive_score, archive_size
    archive_sol.append(solution)
    archive_score[0].append(score[0])
    archive_score[1].append(score[1])
    archive_size += 1

def maintain_archive():
    global archive_sol, archive_score, archive_size
    archive_sol, archive_score, archive_size = maintain_population(archive_sol, archive_score, archive_size)

def maintain_population(decision_space, objective_space, pop_size):
    OS_0 = objective_space[0]
    OS_1 = objective_space[1]

    defenders_DS = []
    defenders_OS_0 = []
    defenders_OS_1 = []

    defenders_DS.append(decision_space[0])
    defenders_OS_0.append(OS_0[0])
    defenders_OS_1.append(OS_1[0])

    nb_defenders = 1
    for challenger in range(1, pop_size):
        challenger_isDominated = False
        defenders_tokill = []
        for defender in range(nb_defenders):
              fight0_result = OS_0[challenger] - defenders_OS_0[defender]
              fight1_result = OS_1[challenger] - defenders_OS_1[defender]
              if(fight0_result >= 0 and fight1_result >= 0): #challenger is dominated by the defender#MIN
                 challenger_isDominated = True
                 break
              elif(fight0_result < 0 and fight1_result < 0): #challenger is dominating the defender #MIN
                 defenders_tokill.append(defender)
              else: #same score
                 pass
        #killing the dominated ones
        nb_defenders_to_kill = len(defenders_tokill)
        for last in range(nb_defenders_to_kill-1, -1, -1 ):
                del defenders_DS[defenders_tokill[last]]
                del defenders_OS_0[defenders_tokill[last]]
                del defenders_OS_1[defenders_tokill[last]]
        nb_defenders -= nb_defenders_to_kill
        #add challenger if not dominated
        if(not(challenger_isDominated)):
            nb_defenders += 1
            defenders_DS.append(decision_space[challenger])
            defenders_OS_0.append(OS_0[challenger])
            defenders_OS_1.append(OS_1[challenger])

    return defenders_DS, [defenders_OS_0, defenders_OS_1], nb_defenders
