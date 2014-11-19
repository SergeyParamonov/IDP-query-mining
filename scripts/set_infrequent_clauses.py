import sys
programfile = sys.argv[1]
program     = open(programfile, "r").read().splitlines()
beginmarker = "INFREQUENT"
endmarker   = "END_OF_INFRQNT_CLAUSES"

for line in program:
  if beginmarker in line:
    begin_index = program.index(line)
  if endmarker in line:
    end_index   = program.index(line)
    break

infrequent_clauses = open(sys.argv[2],"r").read().splitlines()
 
program = program[:begin_index+1] + infrequent_clauses + program[end_index:]
outfile = open(programfile, "w")    
newprogram = "\n".join(program)
outfile.write(newprogram.strip())
outfile.close()
