from random import sample
import sys
#structure_file = "structure.idp"
structure_file = sys.argv[1]
lines          = open(structure_file, "r").read().splitlines()
N                       = int(sys.argv[2])
base_structure_filename = sys.argv[3]
outputfile_name         = sys.argv[4]

def get_graphs(lines):
  graphs     = []
  graph_part = False
  for line in lines:
    if graph_part:
      if "}" in line:
        return graphs
      graph = line.strip(";")
      graphs.append(graph)
    if "graph" in line:
      graph_part = True 
  return graphs

def get_elements(lines, subsample, keyword):
  elems = []
  elems_part = False
  for line in lines:
    if elems_part:
      if "}" in line:
        return elems
      graph = line.split(',')[0].strip()
      if graph in subsample:
        elem = line
        elems.append(elem)
    if keyword in line:
      elems_part = True
  return elems

def get_set_of_labels(label_lines):
  labels = set()
  for label_line in label_lines:
    elems    = label_line.split(",")
    label    = elems[2].strip(";") 
    labels.add(label)
  return labels

def get_graph_nodes(edge_lines):
  graph_nodes = {}
  for line in edge_lines:
    elems = line.split(",")
    graph = elems[0].strip()
    node1 = elems[1].strip()
    node2 = elems[2].strip(" ;")
    if graph:
      graph_nodes.setdefault(graph,set())
      graph_nodes[graph].add(int(node1))
      graph_nodes[graph].add(int(node2))
  return graph_nodes

def generate_zero_edges(graph_nodes):
  graph_edges = []
  for graph in graph_nodes.keys():
    line = str(graph)+","+str(0)+","+str(0) + ";"
    graph_edges.append(line)
    for node in graph_nodes[graph]:
      line = str(graph)+","+str(0)+","+str(node) + ";"
      graph_edges.append(line)
      line = str(graph)+","+str(node) + "," + str(0) + ";"
      graph_edges.append(line)
  return graph_edges

def generate_zero_labels(labels,graphs):
  zero_labels = []
  for graph in graphs:
    for label in labels:
      label_line = graph +","+ str(0) +","+ label + ";"
      zero_labels.append(label_line)
  return zero_labels

def make_graph_idp_line(graphs):
  idp_line = "graph = {"
  for graph in graphs:
    idp_line += graph + ";"
  idp_line = idp_line.strip(";") + "}"
  return idp_line

def make_edge_ipd_line(edge_lines, graph_zero_edges):
  idp_line = "edge = {\n"
  for line in edge_lines:
    idp_line += line +"\n"
# for line in graph_zero_edges:
#   idp_line += line +"\n"
  idp_line = idp_line.strip("\n;") + "\n" + "}"
  return idp_line

def get_all_nodes(graph_nodes):
  nodes = set()
  for graph in graph_nodes.keys():
    nodes |= graph_nodes[graph]
# nodes.add(0)
  return nodes

def make_idp_nodes_line(nodes):
  idp_line = "node = {"
  for node in nodes:
    idp_line += str(node) + ";"
  idp_line = idp_line.strip(";") + "}"
  return idp_line

def make_idp_labels_line(label_lines, zero_labels):
  idp_line = "node_label = {\n"
  for line in label_lines:
    idp_line += line +"\n"
# for line in zero_labels:
#   idp_line += line +"\n"
  idp_line = idp_line.strip("\n;") + "\n" + "}"
  return idp_line


def generate_substructure(graphs, lines, N):
  graph_sample     = sample(graphs, N)
  edge_lines       = get_elements(lines, graph_sample, "edge")
  label_lines      = get_elements(lines, graph_sample, "label")
  labels           = get_set_of_labels(label_lines)
  graph_nodes      = get_graph_nodes(edge_lines)
  allnodes         = get_all_nodes(graph_nodes)
  graph_zero_edges = generate_zero_edges(graph_nodes)
  zero_labels      = generate_zero_labels(labels,graph_sample)
  graph_idp_line   = make_graph_idp_line(graph_sample)
  edge_idp_line    = make_edge_ipd_line(edge_lines, graph_zero_edges)
  node_idp_line    = make_idp_nodes_line(allnodes)
  label_idp_line   = make_idp_labels_line(label_lines, zero_labels)
  idp_substructure = graph_idp_line + "\n" + node_idp_line + "\n" + label_idp_line + "\n" + edge_idp_line + "\n }"
  return idp_substructure
  
graphs = get_graphs(lines)
generated_structure = generate_substructure(graphs, lines, N)
base_structure = open(base_structure_filename, "r").read()
outputfile     = open(outputfile_name,"w")
outputfile.write(base_structure)
outputfile.write(generated_structure)
outputfile.close()
