from __future__ import print_function
import sys

invar_input  = sys.argv[1] 
output_file  = open(sys.argv[2], "a")
invar_prefix = "invar = {"
sol_prefix   = len(invar_prefix)
invars       = invar_input[sol_prefix:].strip(" {}")

if invars:
  invars = map(lambda x: x.strip(' "'), invars.split(";"))

nogood = "~("
for invar in invars:
  nogood += "invar(" + invar +") & "
nogood = nogood.strip(" &")
nogood += ")."
print(nogood, file=output_file)


