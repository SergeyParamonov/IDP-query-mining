data_theta=1
k=120
folder="idp_datasets"
N=2 #number of iterations per dataset
declare -a datasets=( "enzymes" "mutagenesis" "yoshida" "bloodbarr"  "toxinology"  "nctrer" ) #   

for ((j = 0; j < ${#datasets[@]}; j++)); do
  dataset=${datasets[$j]} # get the current dataset
  for ((i=0; i < $N; i++)); do
     logfile=logs/9/logs_${dataset}_$i
     echo "dataset $dataset iteration $i" > $logfile
     timeout 20h ./decomposed_single_run.sh -k $k -d $dataset >> $logfile 
  done
done
