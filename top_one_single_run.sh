#!/bin/bash

while [[ $# > 1 ]]
do
  key="$1"
  shift
  case $key in
    -p)
      positive_N="$1"
      shift
      ;;
    -t|--threshold)
      threshold="$1"
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


if [[ -z $positive_N ]]; then
  positive_N=230
fi

if [[ -z $k ]]; then
  k=10
fi

if [[ -z $threshold ]]; then
  threshold=23
fi

if [[ -z $dataset ]]; then
  dataset="mutagenesis"
fi

scripts=scripts
dataset_folder=idp_datasets

pid=$$
echo "PID $pid"
generated_files=generated/generated_files_${dataset}_$pid
mkdir -p $generated_files

base=base_top_one.idp
python $scripts/make_base_positive.py "$base" $dataset "$generated_files/$base" #print the graph to output
base_positive=$generated_files/$base
python $scripts/set_threshold.py $threshold $base_positive
dataset_positive=$dataset_folder/$dataset

python $scripts/subsample.py $dataset_positive $positive_N $base_positive "$generated_files/positive.idp" ## creates a subsample and save it into the file (2nd arg) in the folder $generated_files 
positive=$generated_files/positive.idp
solution_file=$generated_files/solutions.txt
isomorphism_base=isomorphism.idp
isomorphism=$generated_files/isomorphism.idp
tedge_tlabel=$($scripts/copy_tedge_tlabel.sh $positive)
isomorphism_nogood=$generated_files/isomorphism_breaker.idp

> $solution_file
i=0
while [[ i -lt k ]]; do
  start_time=$(date +%s)
  #candidate generation
# candidate=$(idp $candidate_gen 2>&1 | grep -v "Warning" | grep "invar")
# echo -e "$candidate" 
  echo "iterating..."
  positive_out=$(idp $positive 2>&1 | grep -v "Warning:")
  if [[ "$positive_out" = "nil" ]]; then
    echo "only #$i exist, terminating..." 
    break
  fi
  invar=$(echo "$positive_out" | grep "invar" | python scripts/get_invar.py "$tedge_tlabel" ) # finds one model and gets invar relation out of it, supress warnigns
  echo "$invar"

  python $scripts/generate_no_good.py $positive "$invar"
  #echo "succeeded"
  python $scripts/save_solution.py $solution_file "$invar" 
  (( i++ ))
  cat isomorphism_breaker.idp > $isomorphism_nogood
  python scripts/generate_isomorphism_nogood.py "$invar" "$tedge_tlabel" >> $isomorphism_nogood
  python scripts/set_pattern_length.py $isomorphism_nogood "$invar"
  python $scripts/generate_no_good.py $isomorphism_nogood "$invar" 
  while true; do
    iso_model=$(idp $isomorphism_nogood 2>&1 | grep -v "Warning:")
    if [[ "$iso_model" = "nil" ]]; then
      break
    fi
    iso_invar=$(echo "$iso_model" | grep "invar" | python scripts/get_invar.py "$tedge_tlabel" )
    python $scripts/generate_no_good.py $isomorphism_nogood "$iso_invar" 
    python $scripts/generate_no_good.py $positive "$iso_invar" 
  done
  end_time=$(date +%s)
  runtime=$((end_time-start_time))
  echo "Time: $runtime"
done
cat $solution_file
rm -rf $generated_files
