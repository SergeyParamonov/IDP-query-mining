import sys
base_homo_check = open(sys.argv[1],"r").read()
invars          = sys.argv[2]
graph_data      = open(sys.argv[3], "r").read()
program = open(sys.argv[4], "w")

program.write(base_homo_check+"\n")
program.write(invars+"\n")
program.write(graph_data+"\n")
program.write("}")
program.close()
