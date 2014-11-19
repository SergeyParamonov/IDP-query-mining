from __future__ import print_function
from random import choice
import sys
def make_base(path_to_base, structure_append, outputfilename): 
  program       = open(path_to_base, "r").read()
  new_program   = program + structure_append
  outputfile    = open(outputfilename, "w")
  print(new_program, file=outputfile)
  outputfile.close()
  

def get_template_str(dataset):
  dataset_folder = "idp_datasets/"
  data = open(dataset_folder+dataset, "r").read().splitlines()
  graph_flag = False
  graphs = []
  for line in data:
    if graph_flag and "}" in line:
      break
    if graph_flag:
      graph = line.strip(" ;")
      graphs.append(graph)
    if "graph" in line:
      graph_flag = True
  random_graph = choice(graphs)
  
  edge_flag = False
  tedge     = []
  for line in data:
    if edge_flag and "}" in line:
      break
    if edge_flag:
      g,v1,v2= line.strip(" ;").split(",")
      g = g.strip()
      v1 = v1.strip()
      v2 = v2.strip()
      if g == random_graph and (v2,v1) not in tedge :
        tedge.append((v1,v2))
    if "edge" in line:
      edge_flag = True

  tlabel = []
  label_flag = False
  for line in data:
    if label_flag and "}" in line:
      break
    if label_flag:
      g,v,l = line.strip(" ;").split(",")
      g = g.strip()
      if g == random_graph:
        tlabel.append((v,l))
    if "label" in line:
      label_flag = True

  tedge_str = "t_edge = {"
  for v1,v2 in tedge:
    tedge_str += v1 +"," +v2 +";"
  tedge_str += "}\n"
  tlabel_str   = "t_label = {" 
  for v,l in tlabel:
    tlabel_str += v + "," + l +";"
  tlabel_str  += "}\n"
  structure_append = tedge_str + tlabel_str

  print(tedge) # !!! DELETE IF NECESSARY, JUST PRINTING THE GRAPH TO OUTPUT
  return structure_append
   

path_to_base = sys.argv[1]
template = get_template_str(sys.argv[2])
outbase  = sys.argv[3]
make_base(path_to_base, template, outbase)
