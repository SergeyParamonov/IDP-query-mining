import sys
import re

flag  = False

for line in sys.stdin:
  if "<cf>" in line or "<u>" in line:
    flag = True
    if "<cf>" in line:
      false_invars_str = line
  else:
    print(line)
    sys.exit(0)

tedge        = sys.argv[1]
all_invars   = set(re.findall(r"\d+", tedge))
false_invars = re.findall(r"\d+", false_invars_str)
out_invar = "invar = {"
for invar in all_invars:
  if invar not in false_invars:
    out_invar += str(invar) + ";"

out_invar = out_invar.strip(";")
out_invar += "}"
print(out_invar)
