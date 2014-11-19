#!/bin/bash

data_theta=1
k=1
folder="idp_datasets"
N=10 #number of iterations per dataset
logfolder=logs/top/$RANDOM # use pid to create unique
mkdir -p $logfolder # create the folder for logs
rm -f $logfolder/* # clean the folder
declare -a datasets=( "yoshida" "nctrer"  "bloodbarr"   "mutagenesis" "toxinology" "enzymes" ) #     
for ((j = 0; j < ${#datasets[@]}; j++)); do
  dataset=${datasets[$j]} # get the current dataset
  dataset_size=$(python scripts/get_dataset_size.py $folder/$dataset)
  p=$(python -c "print(int($dataset_size*$data_theta))")
  t=$(python -c "print(int($p*0.05))")
  for ((i=0; i < $N; i++)); do
     log=$logfolder/logs_${dataset}_$i
     echo "dataset: $dataset iteration: $i" >  $log
    ./top_one_single_run.sh -k $k -p $p -t $t -d $dataset  >> $log 
  done
done
