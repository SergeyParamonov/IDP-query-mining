import sys
path_to_dataset = sys.argv[1]
data            = open(path_to_dataset, "r").read().splitlines()
flag_begin = False
counter = 0
for line in data:
  if flag_begin and "}" in line:
    print(counter)
    break
  if flag_begin:
    counter += 1
  if "graph" in line:
    flag_begin = True
