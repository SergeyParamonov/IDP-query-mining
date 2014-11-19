import sys
programfile = sys.argv[1]
program = open(programfile, "r").read()
invar_input   = sys.argv[2] 

invar_prefix  = "invar = {"
sol_prefix    = len(invar_prefix)
invars = invar_input[sol_prefix:].strip(" {}")
if invars:
  invars = map(lambda x: x.strip(' "'), invars.split(";"))

length_of_patter = str(len(invars))
keyword = "LENGTH_OF_PATTERN"

newprogram = program.replace(keyword, length_of_patter)
output = open(programfile, "w")
output.write(newprogram)
output.close()
