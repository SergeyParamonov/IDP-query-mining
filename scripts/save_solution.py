import sys

filename = sys.argv[1]
invar_string = sys.argv[2]

outputfile = open(filename, "a")
outputfile.write(invar_string + "\n")
outputfile.close()

