import sys
program_file = sys.argv[1]
program = open(program_file,"r").read().splitlines()
length  = sys.argv[2]
marker  = "PATTERN_LENGTH"
for line in program:
  if marker in line:
    marker_line = program.index(line)

clause = "  ?" + str(length) + "x: invar(x)."
program[marker_line+1] = clause
newprogram = "\n".join(program)
outfile    = open(program_file, "w")
outfile.write(newprogram)
outfile.close()
