#!/bin/bash

problems="UF1 UF2 UF3"
problem_sizes="10 30"
nb_generations=100
k=1
param_print_every=1

#Folder from where launch every python program
execution_folder=/home/alexandre/Desktop/workspace/Projet_M2/programs_folder
cd "$execution_folder"

#folder that will contain all the experimentation
result_folder="results"
[ ! -d "$execution_folder/$result_folder"  ] && mkdir "$execution_folder/$result_folder"



#complete path to the result folder
current_folder="$execution_folder/$result_folder"

#loop over the problems
parent_problem_folder="$current_folder"
for problem in $problems
do
  [ ! -d "$parent_problem_folder/$problem"  ] && mkdir "$parent_problem_folder/$problem"
  current_folder="$parent_problem_folder/$problem"

  #here we have only one algo : moead
  [ ! -d "$current_folder/moead"  ] && mkdir "$current_folder/moead"
  current_folder="$current_folder/moead"

  #loop over the problem_sizes
  parent_problem_size_folder="$current_folder"
  for problem_size in $problem_sizes
  do
    [ ! -d "$parent_problem_size_folder/$problem_size"  ] && mkdir "$parent_problem_size_folder/$problem_size"
    current_folder="$parent_problem_size_folder/$problem_size"

    #loop over the runs
    for ((i=0; i<$k; i++))
    do
      qsub cluster_no_predict_qsub.sh "$problem" $problem_size $i $nb_generations $param_print_every $current_folder
    done

  done

done
