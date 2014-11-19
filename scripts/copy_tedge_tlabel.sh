source=$1
tedge=$(grep "t_edge = {" $source)
tlabel=$(grep "t_label = {" $source)
echo -e "$tedge \n $tlabel"
