from __future__ import print_function
import sys

filename     = sys.argv[1]
invar_string = sys.argv[2]

program      = open(filename,"r").read()
nogoodmarker = program.index("NOGOODS") + len("NOGOODS") + 1
above_nogood = program[:nogoodmarker]
below_nogood = program[nogoodmarker:]

invar_prefix = len("invar = {") 
invar_string = invar_string[invar_prefix:].strip(""" {}'" """).split(";")
invars = [e.strip(""" "' """) for e in invar_string]
if invars and invars[0] != '':
  nogood = "~("
  for invar in invars:
    nogood  += "invar(" + invar +  ") & "
  nogood = nogood.strip(" &")
  nogood = nogood + ")" + "."
else:
  nogood = "?x: invar(x)."

program_with_nogood = above_nogood + "\n" + nogood + "\n" + below_nogood.strip()
outprogram = open(filename, "w")
print(program_with_nogood, file=outprogram)
