import sys
import re
tedge        = sys.argv[1]
all_invars   = set(re.findall(r"\d+", tedge))
print(len(all_invars))
