import sys
programfile = sys.argv[1]
program     = open(programfile, "r").read().splitlines()
beginmarker = "NOGOODS"
endmarker   = "END_OF_LEARNED_CLAUSES"

for line in program:
  if beginmarker in line:
    begin_index = program.index(line)
  if endmarker in line:
    end_index   = program.index(line)
    break

program    = program[:begin_index+1] + program[end_index:]
newprogram = "\n".join(program).strip("\n")
outfile    = open(programfile, "w")
outfile.write(newprogram)
outfile.close()

