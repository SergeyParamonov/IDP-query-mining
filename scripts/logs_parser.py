from __future__ import print_function
from os import listdir
from os import remove
from os.path import basename
from os.path import isdir, isfile
from numpy import mean, median
#import pandas as pd
import re

def fill_na(times):
  if len(times) >= 100:
    return times
  lentimes = len(times)
  times[lentimes:100] = [ 0 for x in range(lentimes,100)]
  return times
  

def parse_long_logs(filename):
  lines   = open(filename, "r").read().splitlines()
  regexp  = re.compile("dataset (?P<dataset>[\w]+) iteration (?P<iteration>[\d]+)")
  times   = []
  isFirst = True
  iteration = 0
  dataset = ""
  for line in lines:
    if "dataset:" in line:
      if not isFirst:
        frame.to_csv("results/enumeration/"+dataset, index=False)
        print(len(times))
        frame[str(iteration)] = fill_na(times)
        times = []
      frame = pd.DataFrame()
    if "dataset" in line and "iteration" in line:
      if not isFirst: # if it is not the first iteration, save the data
        print(len(times))
        frame[str(iteration)] = fill_na(times)
        times = []
      isFirst = False
      groups    = regexp.match(line)
      dataset   = groups.group("dataset")
      iteration = groups.group("iteration")
      print(dataset + " " + iteration)
    if "Time" in line:
      matched = re.match("Time: (?P<runtime>\d+)", line)
      runtime = matched.group("runtime")
      times.append(runtime)
  print(times)


def parse_short(path):
  filename = basename(path)
  regex = "logs_(?P<dataset>\w+)_(?P<iteration>\d+)"
  matched = re.match(regex, filename)
  print(filename)
  dataset   = matched.group("dataset")
  iteration = matched.group("iteration")
  lines   = open(path, "r").read().splitlines()
  times   = []
  for line in lines:
    if "Time" in line:
      matched = re.match("Time: (?P<runtime>\d+)", line)
      runtime = int(matched.group("runtime"))
      times.append(runtime)
  return dataset, iteration, times

def parse_folder(folder):  
  files = listdir(folder)
  times = {}
  for afile in files:
    if afile[0] != ".":
      dataset, iteration, runtimes = parse_short(folder+"/"+afile)
      times.setdefault(dataset,[])
      times[dataset].append(runtimes) 
  return times

def aggregate(times, outpath):
  for dataset in times.keys():
    aggregated = []
    data = times[dataset] # data is a list of lists
    for i in range(0,100):
      average = mean([time[i] for time in data])
      aggregated.append(average)
    outfile = open(outpath+"/"+dataset, "w")
    for point in aggregated:
      print(point, file=outfile)
    outfile.close()

def clean_logs(logfolder):
  files = listdir(logfolder)
  for afile in files:
    data = open(logfolder+"/"+afile, "r").read()
    if "aborting" not in data:
      remove(afile)

def parse_top_one_recursively(logfolder, outpath):
  files = listdir(logfolder)
  outfile = open(outpath, "a") # needs to be clean
  for afile in files:
    if isfile(logfolder+"/"+afile):
      output = get_top_one(logfolder+"/"+afile)
      if output:
        dataset, runtime = output
        print(dataset + "," +str(runtime), file=outfile)
    elif isdir(logfolder+"/"+afile):
      parse_top_one_recursively(logfolder+"/"+afile, outpath)
  
def get_top_one(path):
  filename  = basename(path)
  regex     = "logs_(?P<dataset>\w+)_(?P<iteration>\d+)"
  matched   = re.match(regex, filename)
  dataset   = matched.group("dataset")

  lines = open(path, "r").read().splitlines()
  runtime = None
  for line in lines:
    if "Time" in line:  
      matched = re.match("Time: (?P<runtime>\d+)", line)
      runtime = matched.group("runtime")
      if runtime:
        break
      else:
        return None
  if runtime:
    return (dataset, runtime)
  else:
    return None
      
def assign_pattern_index(outpath):
  f = open(outpath, "r") # get data
  lines = f.read().splitlines()
  f.close() # and close it, so we can write to the same file
  outfile = open(outpath, "w")
  answer = []
  print("dataset,runtime,dummy_index", file=outfile)
  for line in lines:
    matched   = re.match("(?P<dataset>\w+),(?P<runtime>\d+)", line)
    dataset   = matched.group("dataset")
    runtime   = matched.group("runtime")
    answer.append((dataset,int(runtime)))
  answer.sort()
  times = {}
  for dataset, runtime in answer:
    times.setdefault(dataset,0)
    times[dataset] += 1
    print(dataset+","+str(runtime)+","+str(times[dataset]), file=outfile)
  outfile.close()



#clean the intermediate file results
outpath = "results/top/raw"
outfile = open(outpath, "w") 
outfile.close()
parse_top_one_recursively("logs/top", outpath)
assign_pattern_index(outpath)

#logfolder = "logs/4"
#clean_logs(logfolder)  
#times = parse_folder(logfolder)
#aggregate(times,"results/enumeration")

#parse_long_logs("logs.txt")
