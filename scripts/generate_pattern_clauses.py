from __future__ import print_function
import sys
solutions_raw = open(sys.argv[1], "r").read().split("\n")
invar_raw     = sys.argv[2]
tedge_labels  = sys.argv[3].split("\n")
edge_prefix   = "t_edge = {"
label_prefix  = "t_label = {"
invar_prefix  = "invar = {"
sol_prefix    = len(invar_prefix)

#invar processing 
invars = invar_raw[sol_prefix:].strip(" {}")
if invars:
  invars = map(lambda x: x.strip(' "'), invars.split(";"))

#t_edge and t_label processing
edges = []
labels = []
for line in tedge_labels:
  if edge_prefix in line:
    edges_raw = map(lambda x: x.strip(' "{}'), line[len(edge_prefix):].split(";"))
    for edge in edges_raw:
      if edge:
        x,y = edge.split(",")
        edges.append((x,y))
  if label_prefix in line:
    labels_raw = map(lambda x: x.strip(' "{}'), line[len(label_prefix):].split(";"))
    for label in labels_raw:
      if label:
        x,l = label.split(",")
        labels.append((x,l))

#processing of previous solutions in the form of invar = { .... }
solutions = []
for solution in solutions_raw:
  if solution:
    solution  = solution[sol_prefix:].strip(" {}")
    variables = map(lambda x: x.strip(' "'), solution.split(";"))
    solutions.append(variables)

#generate solution patterns 
print("edge = {")
for solution in solutions:
  i = solutions.index(solution) + 1
  for edge in edges:
    x,y = edge
    if x in solution and y in solution:
      print(str(i)+","+x+","+y+";") 
      print(str(i)+","+y+","+x+";") 
print("}")

print("n_label = {")
for solution in solutions:
  i = solutions.index(solution) + 1
  for label in labels:
    x,l = label
    print(str(i) + "," + x + " -> " + l + ";") 
print("}")


print("pattern = {")
for edge in edges:
  x,y = edge
  if x in invars and y in invars:
    print(x + "," + y + ";")
    print(y + "," + x + ";")
print("}") 

print("p_label = {")
for label in labels:
  x,l = label
  if x in invars:
    print(x + " -> " + l + ";")
print("}")
print("}")
