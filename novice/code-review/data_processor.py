import os
import sys

import numpy as np
from matplotlib import pyplot

def read_csv_file(input_csv_file):
    '''
    This code will read in a csv file of year, temperature, rainfall,
    and number of mosquitos and return 4 arrays, one for each column
    '''
    return np.genfromtxt(input_csv_file, unpack=True,skiprows=1,delimiter=",")
    years, temperature, rainfall, mosquitos = d
    return d

def process(dataset):
    '''
    process the data file and output the necessary analytics

    we want standard deviation and variance for each column
    '''
    data = []
    for arr_arr in dataset:
      std_arr_arr = np.sqrt(np.mean(abs(arr_arr - np.mean(arr_arr)) * 2));
      var_arr_arr = (np.mean(abs(arr_arr - np.mean(arr_arr)) ** 2));
      max_arr_arr = max(arr_arr);
      min_arr_arr = min(arr_arr);
      print max_arr_arr, min_arr_arr;
      data.append([std_arr_arr, var_arr_arr]);
    return data

def write_file(ofile, data):
    ofile = open(ofile, 'w')
    for row in data:
        ofile.write(np.array_str(np.array(row)))
    ofile.close()

# sys.argv contains all the parameters passed
# to the program. assume the 1st is a filename
# this way we can use the same file for many datasets!
input_file = sys.argv[1]
ofile = "processed-" + input_file
if not input_file:
    print "need a file to process!"
    exit(1)
p = read_csv_file(input_file)
pr = process(p)
write_file(ofile, pr)
