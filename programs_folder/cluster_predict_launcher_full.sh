#!/bin/bash

fruit=true

if $fruit then
    algorithms="NuSVR-freeeval"
    filters="AvScl AvSclNormG AvImprG BestScl BestImprG by_direction NumberImpr AvImprNormG BestSclNormG BestImprNormG"
    lambdas="2 4 8 16 32"
    problems="UF3"
    problem_sizes="10"
    nb_generations=100
    k=30
else
    algorithms="NuSVR-pop NuSVR-newest NuSVR-popnewest"
    #filters="AvScl AvSclNormG AvSclNormP AvImprG AvImprP BestScl BestImprP BestImprG by_direction NumberImpr NumberImprP AvImprNormG AvImprNormP BestSclNormG BestSclNormP BestImprNormG BestImprNormP"
    filters="AvScl AvSclNormG AvSclNormP AvImprG AvImprP BestScl BestImprP BestImprG by_direction NumberImpr NumberImprP"
    lambdas="2 4 8 16 32"
    problems="UF3"
    problem_sizes="10"
    nb_generations=100
    k=30
fi
#algorithms="NuSVR-freeeval"
#filters="average"
#trainings="single"
#lambdas="2"
#problems="UF1 "
#problem_sizes="10"
#nb_generations=100
#k=1 
param_print_every=1
trainings="single"
fe="freeeval"



#Folder from where launch every python program
execution_folder=/home/alexander/Desktop/Projet_M2/programs_folder
cd "$execution_folder"

#folder that will contain all the experimentation
result_folder="results_byQ2"
[ ! -d "$execution_folder/$result_folder"  ] && mkdir "$execution_folder/$result_folder"



#complete path to the result folder
current_folder="$execution_folder/$result_folder"

#loop over the problems
parent_problem_folder="$current_folder"
for problem in $problems
do
    [ ! -d "$parent_problem_folder/$problem"  ] && mkdir "$parent_problem_folder/$problem"
    current_folder="$parent_problem_folder/$problem"


    #loop over the algorithms
    parent_algorithm_folder="$current_folder"
    for algorithm in $algorithms
    do
        #here we have only one algo : moead
        [ ! -d "$parent_algorithm_folder/$algorithm"  ] && mkdir "$parent_algorithm_folder/$algorithm"
        current_folder="$parent_algorithm_folder/$algorithm"

        if test "${algorithm#*$fe}" != "$algorithm"
        then
                              #loop over the filters
                              parent_filter_folder="$current_folder"
                              for filter in $filters
                              do
                                  [ ! -d "$parent_filter_folder/$filter"  ] && mkdir "$parent_filter_folder/$filter"
                                  current_folder="$parent_filter_folder/$filter"

                                  #loop over the lambdas
                                  parent_lambda_folder="$current_folder"
                                  for lambda in $lambdas
                                  do
                                      [ ! -d "$parent_lambda_folder/$lambda"  ] && mkdir "$parent_lambda_folder/$lambda"
                                      current_folder="$parent_lambda_folder/$lambda"

                                      #loop over the problem_sizes
                                      parent_problem_size_folder="$current_folder"
                                      for problem_size in $problem_sizes
                                      do
                                          [ ! -d "$parent_problem_size_folder/$problem_size"  ] && mkdir "$parent_problem_size_folder/$problem_size"
                                          current_folder="$parent_problem_size_folder/$problem_size"

                                          #loop over the runs
                                          for ((i=0; i<$k; i++))
                                          do
                                              #echo "$current_folder"
                                              qsub cluster_predict_qsub.sh "$problem" "$algorithm" $problem_size "single" $lambda "$filter" $i $nb_generations $param_print_every "$current_folder"
                                          done
                                      done
                                  done
                              done
        else

                    #loop over the trainings
                    parent_training_folder="$current_folder"
                    for training in $trainings
                    do
                        [ ! -d "$parent_training_folder/$training"  ] && mkdir "$parent_training_folder/$training"
                        current_folder="$parent_training_folder/$training"

                        #loop over the filters
                        parent_filter_folder="$current_folder"
                        for filter in $filters
                        do
                            [ ! -d "$parent_filter_folder/$filter"  ] && mkdir "$parent_filter_folder/$filter"
                            current_folder="$parent_filter_folder/$filter"

                            #loop over the lambdas
                            parent_lambda_folder="$current_folder"
                            for lambda in $lambdas
                            do
                                [ ! -d "$parent_lambda_folder/$lambda"  ] && mkdir "$parent_lambda_folder/$lambda"
                                current_folder="$parent_lambda_folder/$lambda"

                                #loop over the problem_sizes
                                parent_problem_size_folder="$current_folder"
                                for problem_size in $problem_sizes
                                do
                                    [ ! -d "$parent_problem_size_folder/$problem_size"  ] && mkdir "$parent_problem_size_folder/$problem_size"
                                    current_folder="$parent_problem_size_folder/$problem_size"

                                    #loop over the runs
                                    for ((i=0; i<$k; i++))
                                    do
                                        #echo "$current_folder"
                                        qsub cluster_predict_qsub.sh "$problem" "$algorithm" $problem_size "$training" $lambda "$filter" $i $nb_generations $param_print_every $current_folder
                                    done
                                done
                            done
                        done
                    done
        fi
    done

done
