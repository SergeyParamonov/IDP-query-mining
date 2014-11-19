#!/bin/bash

while [[ $# > 1 ]]
do
  key="$1"
  shift
  case $key in
    -t|--threshold)
      data_theta="$1"
      shift
      ;;
    -k)
      k="$1"
      shift
      ;;
    -d)
      dataset="$1"
      shift
      ;;
  esac
done


if [[ -z $k ]]; then
  k=100
fi

if [[ -z $threshold ]]; then
  data_theta=0.1
fi

if [[ -z $dataset ]]; then
  dataset="mutagenesis"
fi

scripts=scripts/
dataset_folder=idp_datasets
pid=$$
echo "PID $pid"
generated_files=generated/generated_files$pid/
mkdir -p $generated_files
python scripts/make_base_positive.py "candidate_generation.idp" $dataset "$generated_files/base.idp" #print the graph to output
base=$generated_files/base.idp 
echo "}" >> $base # finishing the structure
dataset_positive=$dataset_folder/$dataset

positive=$generated_files/positive.idp
solution_file=$generated_files/solutions.txt
tedge_tlabel=$(scripts/copy_tedge_tlabel.sh $base)
template_length=$(python scripts/get_tedge_length.py "$tedge_tlabel")
isomorphism_nogood=$generated_files/isomorphism_breaker.idp
homobase=$generated_files/homo_base
cat homo_base.idp > $homobase
echo "$tedge_tlabel" >> $homobase
homocheck=$generated_files/homo_check.idp
data_path=decomposed_datasets/$dataset
homoout=$generated_files/aggregate
infrequent_nogoods=$generated_files/infrequent_nogoods
dataset_size=$(python scripts/get_dataset_size.py $dataset_folder/$dataset)
threshold=$(python -c "print(int($dataset_size*$data_theta))")

> $solution_file
> $infrequent_nogoods
i=2
echo "iterating length: $i"
python scripts/set_length_clause.py $base $i #initial length is set to 1
template_length=13
while [[ i -le template_length ]]; do
  start_time=$(date +%s)
  if (( k == 0 )); then
    echo "mined specified number of patterns... aborting"
    break
  else
    (( k-- ))
  fi
  candidate=$(idp $base 2>&1 | grep -v "Warning:")
  if [[ "$candidate" = "nil" ]]; then
    echo "mined all patterns of length: $i" 
    (( i++ ))
    python scripts/forget_nogoods.py $base
    python scripts/set_length_clause.py $base $i
    python scripts/set_infrequent_clauses.py $base $infrequent_nogoods
    echo "iterating length: $i"
    continue
  fi
  invar=$(echo "$candidate" | grep "invar" | python scripts/get_invar.py "$tedge_tlabel") # finds one model and gets invar relation out of it, supress warnigns
  echo "$invar"

  #processing aggregate file
  cat aggregate_base.idp > $homoout
  sed -i "s/NUMBER/$threshold/" $homoout
  echo "pattern_in = {" >> $homoout
  # checking presence of homomorphisms
  matched=0
  for graph in $data_path/*; do
    python scripts/make_homo_program.py $homobase "$invar" $graph $homocheck
    model=$(idp "$homocheck" 2>&1 | grep -v "Warning:")
    if [[ "$model" != "nil" ]]; then
      (( matched++ ))
      graph_name=$(basename $graph)
      echo "$graph_name;" >> $homoout
      if [[ matched -ge threshold ]]; then  #
        break                               # check only up to threshold occurances 
      fi                                    #
    fi
  done
  #finishind processing of aggregate file
  echo "}" >> $homoout
  echo "}" >> $homoout
  # aggregation
  aggregation=$(idp $homoout 2>&1 | grep -v "Warning:")
  infrequent=false
  if [[ "$aggregation" != "nil" ]]; then
    echo "frequent"
  else
    echo "not frequent"
    infrequent=true
    python scripts/infrequent_nogood.py "$invar" $infrequent_nogoods
  fi
  echo "$k patterns left"
  
  # no-good learning
  python scripts/generate_classic_nogood.py $base "$invar"
  python scripts/save_solution.py $solution_file "$invar" 
  # isomorphism handling
  cat isomorphism_breaker.idp > $isomorphism_nogood
  python scripts/generate_isomorphism_nogood.py "$invar" "$tedge_tlabel" >> $isomorphism_nogood
  python scripts/set_pattern_length.py $isomorphism_nogood "$invar"
  python scripts/generate_classic_nogood.py $isomorphism_nogood "$invar" 
  while true; do
    iso_model=$(idp $isomorphism_nogood 2>&1 | grep -v "Warning:")
    if [[ "$iso_model" = "nil" ]]; then
      break
    fi
    iso_invar=$(echo "$iso_model" | grep "invar" | python scripts/get_invar.py "$tedge_tlabel")
    python scripts/generate_classic_nogood.py $isomorphism_nogood "$iso_invar" 
    python scripts/generate_classic_nogood.py $base "$iso_invar" 
    if [ $infrequent = true ]; then
      echo $infrequent
      echo "infrequent iso"
      python scripts/infrequent_nogood.py "$iso_invar" $infrequent_nogoods
    fi
  done
  end_time=$(date +%s)
  runtime=$((end_time-start_time))
  echo "Time: $runtime"
done
rm -rf generated_files$pid
