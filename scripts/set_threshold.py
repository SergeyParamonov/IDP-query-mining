from __future__ import print_function
import sys

threshold = sys.argv[1]
basefile  = sys.argv[2]

base_program  = open(basefile, "r").read()
threshold_str = "\nthreshold = " + threshold
base_program += threshold_str
base_out      = open(basefile, "w")
print(base_program, file=base_out)
base_out.close()

