import sys, re
from optparse import OptionParser
import time
import os
import getopt
import numpy  as np
from scipy import stats

data = []

def save_data(filename, column1, column2):
  with open(filename, 'w') as f:
    for a,b in zip(column1,column2):
      f.write(str(a)+ "\t" + str(b) + "\n")
  
def help_function():
  
  print(" -f filename to process")
  print(" -o output filename")



def process_file(filename):
  val_temp = []
  with open(filename, 'r') as f:
      lines = f.readlines()
      for line in lines:
        val_temp.append(float(line.replace("\n", "").split()[0]))
  return val_temp
  
def main(argv):
  
  current_dir = "./"

  list_dir = []
  
  for filename in os.listdir(current_dir):
    if os.path.isdir(os.path.join(current_dir,filename)):
        print(filename)
        list_dir.append(filename)
  
  
  string_file = ""
  output = ""
  try:
     opts, args = getopt.getopt(sys.argv[1:],"hf:o:",["file=","output="])
  except getopt.GetoptError as err:
     # print (str(err))
     sys.exit(2)
  for opt, arg in opts:
      if opt == '-h':
          help_function()
          sys.exit()
      elif opt in ("-f", "--file"):
          string_file= arg
      elif opt in ("-o", "--label"):
          output = arg
      

  if (output =="" or string_file == ""):
    help_function()
    exit()
  
  matrix_val = []
  for directory in list_dir:
    if directory.startswith('.'):
      continue
    directory = (os.path.join(current_dir,directory))
    print(directory)
    matrix_val.append(process_file(os.path.join(directory, string_file)))

  assert([len(matrix_val[0])==len(i) for i in matrix_val])
  
  matrix_val = np.array(matrix_val)
  print(matrix_val)
  print(matrix_val.shape)

  mean_array = np.mean(matrix_val, axis=0)
  stddev_array = np.std(matrix_val, axis=0) 
  sem = stats.sem(matrix_val, axis=0, ddof=0)
  
  save_data(os.path.join(current_dir,output), mean_array, sem)
  save_data(os.path.join(current_dir,output), mean_array, stddev_array)
  
if __name__ == '__main__':
  main(sys.argv[1:])
