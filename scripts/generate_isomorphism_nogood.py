from __future__ import print_function
import sys
invar_raw     = sys.argv[1]
tedge_labels  = sys.argv[2].split("\n")
edge_prefix   = "t_edge = {"
label_prefix  = "t_label = {"
invar_prefix  = "invar = {"
sol_prefix    = len(invar_prefix)

# invar processing 
invars = invar_raw[sol_prefix:].strip(" {}")
if invars:
  invars = map(lambda x: x.strip(' "'), invars.split(";"))

# t_edge and t_label processing
edges = []
labels = []
pnodes = set()
for line in tedge_labels:
  if edge_prefix in line:
    edges_raw = map(lambda x: x.strip(' "{}'), line[len(edge_prefix):].split(";"))
    for edge in edges_raw:
      if edge:
        x,y = edge.split(",")
        pnodes.add(x); pnodes.add(y)
        edges.append((x,y))
  if label_prefix in line:
    labels_raw = map(lambda x: x.strip(' "{}'), line[len(label_prefix):].split(";"))
    for label in labels_raw:
      if label:
        x,l = label.split(",")
        labels.append((x,l))

print("pattern = {", end="")
for edge in edges:
  x,y = edge
  if x in invars and y in invars:
    print(x + "," + y + ";",end="")
    print(y + "," + x + ";",end="")
print("}") 

print("pnode = {", end="")
for x in invars:
  print(x + ";", end="")
print("}")

print("p_label = {", end="")
for x,l in labels:
  if x in invars:
    print(x + "," + l + ";", end="")
print("}")

print("t_edge = {", end="")
for edge in edges:
  x,y = edge
  print(x + "," + y + ";",end="")
  print(y + "," + x + ";",end="")
print("}")

print("label = {", end="")
for x,l in labels:
  print(x + "," + l + ";", end="")
print("}")

#close the structure
print("}")


