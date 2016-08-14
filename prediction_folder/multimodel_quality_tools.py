import numpy as np


predictions = []
true_scores = []
nb_of_models = -1
nb_of_generations = -1
nb_of_directions = -1
filenameDIR = -1
filenameSCORE = -1
score_towrite_tab = []

def computeQualityEvaluation():
    global predictions, true_scores, nb_of_generations, nb_of_directions, nb_of_models

    for m in range(nb_of_models):
        towrite = []
        towriteSTAR = []
        for g in range(nb_of_generations):
            nb_off_predict_star  = 0.0
            sum_mse_star         = 0.0
            sum_mae_star         = 0.0
            sum_DMAE_star        = 0.0
            sum_tcheby_pred_star = 0.0
            sum_tcheby_free_star = 0.0
            ss_tot_star          = 0.0
            ss_reg_star          = 0.0
            ss_res_star          = 0.0

            for d in range(nb_of_directions):
                sum_mse         = 0.0
                sum_mae         = 0.0
                sum_DMAE        = 0.0
                sum_tcheby_free = 0.0
                sum_tcheby_pred = 0.0
                ss_tot          = 0.0
                ss_reg          = 0.0
                ss_res          = 0.0

                nb_off_predict_for_d = len(predictions[m][g][d])
                #print(g,d, nb_off_predict_for_d)
                nb_off_predict_star += nb_off_predict_for_d
                for o in range(nb_off_predict_for_d):
                    tmp_mse          = (predictions[m][g][d][o] - true_scores[m][g][d][o])**2
                    sum_mse         += tmp_mse

                    tmp_mae          = abs(predictions[m][g][d][o] - true_scores[m][g][d][o])
                    sum_mae         += tmp_mae

                    tmp_DMAE         = abs( (predictions[m][g][d][o] - true_scores[m][g][d][o]) / true_scores[m][g][d][o] )
                    sum_DMAE        += tmp_DMAE

                    sum_tcheby_pred += predictions[m][g][d][o]
                    sum_tcheby_free += true_scores[m][g][d][o]

                y_barre = sum_tcheby_free / nb_off_predict_for_d
                for o in range(nb_off_predict_for_d):
                    ss_tot += ( true_scores[m][g][d][o] - y_barre                 )**2
                    ss_reg += ( predictions[m][g][d][o] - y_barre                 )**2
                    ss_res += ( true_scores[m][g][d][o] - predictions[m][g][d][o] )**2

                sum_mse_star         += sum_mse
                sum_mae_star         += sum_mae
                sum_DMAE_star        += sum_DMAE
                sum_tcheby_pred_star += sum_tcheby_pred
                sum_tcheby_free_star += sum_tcheby_free
                ss_tot_star          += ss_tot
                ss_reg_star          += ss_reg
                ss_res_star          += ss_res

                towrite.append( str(g) )
                towrite.append( ' ' )
                towrite.append( str(d) )
                towrite.append( ' ' )
                towrite.append( str( sum_mse         / nb_off_predict_for_d) )
                towrite.append( ' ' )
                towrite.append( str( sum_mae         / nb_off_predict_for_d) )
                towrite.append( ' ' )
                towrite.append( str( sum_DMAE        / nb_off_predict_for_d) )
                towrite.append( ' ' )
                towrite.append( str( sum_tcheby_pred / nb_off_predict_for_d) )
                towrite.append( ' ' )
                towrite.append( str( sum_tcheby_free / nb_off_predict_for_d) )
                towrite.append( ' ' )
                towrite.append( str( ss_tot ) )
                towrite.append( ' ' )
                towrite.append( str( ss_reg ) )
                towrite.append( ' ' )
                towrite.append( str( ss_res ) )
                towrite.append( '\n' )
            towriteSTAR.append( str( g ) )
            towriteSTAR.append(' ')
            towriteSTAR.append("*")
            towriteSTAR.append(' ')
            towriteSTAR.append( str( sum_mse_star         / nb_off_predict_star ) )
            towriteSTAR.append(' ')
            towriteSTAR.append( str( sum_mae_star         / nb_off_predict_star ) )
            towriteSTAR.append( ' ' )
            towriteSTAR.append( str( sum_DMAE_star        / nb_off_predict_star ) )
            towriteSTAR.append( ' ' )
            towriteSTAR.append( str( sum_tcheby_pred_star / nb_off_predict_star ) )
            towriteSTAR.append( ' ' )
            towriteSTAR.append( str( sum_tcheby_free_star / nb_off_predict_star ) )
            towriteSTAR.append( ' ' )
            towriteSTAR.append( str( ss_tot_star ) )
            towriteSTAR.append( ' ' )
            towriteSTAR.append( str( ss_reg_star ) )
            towriteSTAR.append( ' ' )
            towriteSTAR.append( str( ss_res_star ) )
            towriteSTAR.append( '\n' )


        filenameDIR_corrected = filenameDIR.replace("DIR_UF", ("DIR-model" + str(m+1) + "_UF"))
        fd = open(filenameDIR_corrected, 'a')
        fd.write(''.join(towrite))
        fd.close()
        filenameDIRSTAR = filenameDIR.replace("DIR_UF", ("DIRSTAR-model" + str(m+1) + "_UF"))
        fd = open(filenameDIRSTAR, 'a')
        fd.write(''.join(towriteSTAR))
        fd.close()

def resetGlobalVariables(filenameD, filenameS , nb_g, nb_d, objective_quantity):
    global predictions, true_scores, filenameDIR, nb_of_generations, nb_of_directions, filenameSCORE, nb_of_models
    filenameSCORE = filenameS
    score_towrite_tab = []
    filenameDIR = filenameD
    predictions = []
    true_scores = []
    nb_of_models = objective_quantity
    nb_of_directions = nb_d
    nb_of_generations = nb_g
    for m in range(nb_of_models):
        predictions.append([])
        true_scores.append([])
        for g in range(nb_of_generations):
            predictions[m].append([])
            true_scores[m].append([])
            for d in range(nb_of_directions):
                predictions[m][g].append([])
                true_scores[m][g].append([])

def generateDiffPredFreeFile():
    global filenameSCORE, score_towrite_tab
    fd = open(filenameSCORE, 'a')
    fd.write(''.join(score_towrite_tab))
    fd.close()

def addToScoreTab(current_g, current_f, score_best_pred, save_best_pred_free_score, index_best_pred, score_best_free, save_best_free_pred_score,  index_best_free):
    score_towrite_tab.append(str(current_g))
    score_towrite_tab.append(' ')
    score_towrite_tab.append(str(current_f))
    score_towrite_tab.append(' ')
    score_towrite_tab.append(str(score_best_pred))
    score_towrite_tab.append(' ')
    score_towrite_tab.append(str(save_best_pred_free_score))
    score_towrite_tab.append(' ')
    score_towrite_tab.append(str(save_best_free_pred_score))
    score_towrite_tab.append(' ')
    score_towrite_tab.append(str(score_best_free))
    score_towrite_tab.append(' ')
    score_towrite_tab.append('1' if index_best_pred == index_best_free else '0')
    score_towrite_tab.append('\n')

def add(generation, direction, pred_objectivevectors, free_objectivevectors, objective_quantity):
    nb_objectivevectors = len(free_objectivevectors)
    for m in range(0, objective_quantity):
        predictions[m][generation][direction].extend(pred_objectivevectors[m].tolist())
        for j in range(0, nb_objectivevectors):
            true_scores[m][generation][direction].append(free_objectivevectors[j][m])
