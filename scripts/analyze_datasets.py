from __future__ import print_function
from os import listdir
def number_of(keyword, data):
  flag_begin = False
  count = 0 
  for line in data:
    if flag_begin and "}" in line:
      break
    if flag_begin:
      count += 1
    if keyword in line:
      flag_begin = True
  return count

def count_vertices_labels(data):
  vertices = {}
  labels   = set()
  flag_begin = False
  for line in data:
    if flag_begin and "}" in line:
      break
    if flag_begin:
      g,v,l = line.strip(" ;").split(",")
      g = g.strip()
      labels.add(l)
      vertices.setdefault(g,0)
      vertices[g] += 1
    if "label" in line:
      flag_begin = True
  return vertices, labels

def count_edges(data):
  edges = {}
  flag_begin = False
  for line in data:
    if flag_begin and "}" in line:
      break
    if flag_begin:
      g,v1,v2 = line.strip(" ;").split(",")
      g = g.strip()
      edges.setdefault(g,0)
      edges[g] += 1
    if "edge" in line:
      flag_begin = True
  return edges


folder = "../idp_datasets/"
for dataset in listdir(folder):
  print(dataset)
  data = open(folder+dataset, "r").read().splitlines()
  n_graph = number_of("graph", data)
  n_edge  = int(number_of("edge", data)/2)
  avg_edge = n_edge/float(n_graph)
  v, l    = count_vertices_labels(data)
  num_v   = sum(v.values())
  avg_v   = num_v/float(n_graph)
  e       = count_edges(data)
  d       = [e[g]/(2*float(v[g])) for g in v.keys()]
# print(sum(d)/float(len(d)))
# print(d)
  print("Avg N of v: " + str(avg_v))
  print("Num of labels " + str(len(l)))
  print("Num of graphs " + str(n_graph))
  print("Num of edges "  + str(avg_edge))
