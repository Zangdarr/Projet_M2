import numpy


predictions = []
true_scores = []
nb_of_generations = -1
nb_of_directions = -1
filenameDIR = -1

def computeQualityEvaluation():
    global predictions, true_scores, nb_of_generations, nb_of_directions
    nb_off_predict_star = 0
    sum_mse_star = 0.0
    sum_mae_star = 0.0

    towrite = []

    for g in range(nb_of_generations):
        for d in range(nb_of_directions):
            sum_mse = 0.0
            sum_mae = 0.0
            nb_off_predict_for_d = len(predictions[g][d])
            print(g,d, nb_off_predict_for_d)
            nb_off_predict_star += nb_off_predict_for_d
            for o in range(nb_off_predict_for_d):
                tmp_mse       = (predictions[g][d][o] - true_scores[g][d][o])**2
                sum_mse      += tmp_mse
                sum_mse_star += tmp_mse

                tmp_mae       = abs(predictions[g][d][o] - true_scores[g][d][o])
                sum_mae      += tmp_mae
                sum_mae_star += tmp_mae

            towrite.append(str(g))
            towrite.append( ' ' )
            towrite.append(str(d))
            towrite.append( ' ' )
            towrite.append( str(sum_mse / nb_off_predict_for_d) )
            towrite.append( ' ' )
            towrite.append( str(sum_mae / nb_off_predict_for_d) )
            towrite.append( '\n' )
    towrite.append("gggggggggggstar")
    towrite.append(' ')
    towrite.append("ddddddddddddstar")
    towrite.append(' ')
    towrite.append( str(sum_mse_star / nb_off_predict_star) )
    towrite.append(' ')
    towrite.append( str(sum_mae_star / nb_off_predict_star) )

    fd = open(filenameDIR, 'a')
    fd.write(''.join(towrite))
    fd.close()

def resetGlobalVariables(filename, nb_g, nb_d):
    global predictions, true_scores, filenameDIR, nb_of_generations, nb_of_directions
    filenameDIR = filename
    predictions = []
    true_scores = []
    nb_of_directions = nb_d
    nb_of_generations = nb_g
    for g in range(nb_of_generations):
        predictions.append([])
        true_scores.append([])
        for d in range(nb_of_directions):
            predictions[g].append([])
            true_scores[g].append([])


def add(generation, direction, predict_score, true_score_oldzstar):
    predictions[generation][direction].append(predict_score)
    true_scores[generation][direction].append(true_score_oldzstar)
