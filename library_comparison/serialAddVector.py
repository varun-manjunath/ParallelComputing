# Author: Varun M
# Parallel computing library comparison 2017
# https://github.com/varun-manjunath/ParallelComputing/tree/master/library_comparison

import sys
import time
import pickle

# Get the current test case from command line arguments
test_case_num=int(sys.argv[1])

# load the pickled lists from .pkl files
x=pickle.load(open('test_case_'+str(test_case_num)+'_x.pkl','rb'))
y=pickle.load(open('test_case_'+str(test_case_num)+'_y.pkl','rb'))

# create a output list based on input data
size=len(x)
z=[0]*size

# Record start time
before=time.time()

# Vector sum computation
for i in range(0,size):
	z[i]=x[i]+y[i]

# Record end time and write to out file
timeElapsed=time.time()-before
with open('py_serial.out','a') as outFile:
	outFile.write(str(timeElapsed)+'\n')

print(size,'Python serial time:',timeElapsed,'seconds')
# print(z)