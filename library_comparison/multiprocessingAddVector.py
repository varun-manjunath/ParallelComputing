# Author: Varun M
# Parallel computing library comparison 2017
# https://github.com/varun-manjunath/ParallelComputing/tree/master/library_comparison

import sys
import time
import pickle
import multiprocessing

# Get the current test case from command line arguments
test_case_num=int(sys.argv[1])

# load the pickled lists from .pkl files
x=pickle.load(open('test_case_'+str(test_case_num)+'_x.pkl','rb'))
y=pickle.load(open('test_case_'+str(test_case_num)+'_y.pkl','rb'))

workSize=len(x)

# Array is a shared memory C style array, first parameter defines type of elements
# 'i' for integers
z=multiprocessing.Array('i',(0,)*workSize,lock=False)

# each `multiprocessing` spawned process will execute this function for it's allocated shared array chunk
def sum(block):
	for i in range(*block):
			z[i]=x[i]+y[i]

before=time.time()

# Create a process pool
pool=multiprocessing.Pool()

# list to store all applyResult objects
results=[]

# set the number of process workers
numProcesses=4

#get size of block for data split parallelism
blockSize=workSize//numProcesses
for i in range(0,numProcesses):
	myStartBlock=i*blockSize
	# Invoke an asynchronous process and expect output in ApplyResult list 'results'
	results.append(pool.apply_async(sum,((myStartBlock,myStartBlock+blockSize),)))

#check and retrieve the asynchronous status of each process
for applyResult in results:
	# applyResult.get(timeout=3)
	# blocking call
	applyResult.get()

# Record end time and write to out file
timeElapsed=time.time()-before
with open('py_multiprocessing.out','a') as outFile:
	outFile.write(str(timeElapsed)+'\n')

print(workSize,'Python multiprocessing time:',timeElapsed,'seconds')
# print(z)