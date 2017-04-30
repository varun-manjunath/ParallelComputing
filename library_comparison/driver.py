# Author: Varun M
# Parallel computing library comparison 2017
# https://github.com/varun-manjunath/ParallelComputing/tree/master/library_comparison

import sys
import os
import pickle
import random
from statistics import mean

# Clean up program outputs for each new benchmark
out_files=['c_serial.out','c_openMP.out','c_pthread.out','py_serial.out','py_pyMP.out','py_multiprocessing.out']
for out_file in out_files:
	if os.path.exists(out_file):
		os.remove(out_file)
		print('Removed',out_file)

print()

r=random.Random()
testCaseCount=5
# 5 test cases
for i in range(1,testCaseCount+1):
	arraySize=10**(i+3)
	
	# 100000000 element long array is too large, so reduce by half!
	if i==5:
		arraySize//=2

	testList=[0]*arraySize
	arraySizeString=str(arraySize)
	commands=['gcc serialAddVector.c;./a.out','gcc -fopenmp openMPAddVector.c;./a.out','gcc -pthread pthreadAddVector.c;./a.out','python serialAddVector.py '+str(i),'python pyMPAddVector.py '+str(i),'python multiprocessingAddVector.py '+str(i)]
	prefix='test_case_'+str(i)+'_'
	
	# Create a header file to describe current test case during C program execution
	with open('comparison.h','w') as headerFile:
		headerFile.write('// This file is auto-generated!\n// Please do not modify values and expect them to persist across program executions!  :)\n\n')
		headerFile.write('long array_size='+str(arraySize)+';\n')
		headerFile.write('char x_test_case_file_name[100]="'+prefix+'x.txt'+'";\n')
		headerFile.write('char y_test_case_file_name[100]="'+prefix+'y.txt'+'";\n')
		
	# Write the `x` array test case data into a file to be used by test programs
	with open(prefix+'x'+'.txt','w') as xFile:
		for k in range(arraySize):
			temp=r.randint(0,512)
			testList[k]=temp
			xFile.write(str(temp)+'\n')

	# using testList pickling to quickly load random integers into the Python programs
	with open(prefix+'x.pkl','wb') as xPickleFile:
		pickle.dump(testList,xPickleFile)

	# Write the `y` array test case data into a file to be used by test programs
	with open(prefix+'y.txt','w') as yFile:
		for k in range(arraySize):
			temp=r.randint(0,512)
			testList[k]=temp
			yFile.write(str(temp)+'\n')

	# using testList pickling to quickly load random integers into the Python programs
	with open(prefix+'y.pkl','wb') as yPickleFile:
		pickle.dump(testList,yPickleFile)

	# Execute all the test programs
	for command in commands:
		# 3 runs for each test case
		for j in range(3):
			os.system(command)
	print()

#Test average runtime for all test cases... Just a statistical mean; comparing amongst particular test cases is better!
print('Final C serial time:',mean(map(float,open('c_serial.out','r').read().strip().split('\n'))))
print('Final C openMP time:',mean(map(float,open('c_openMP.out','r').read().strip().split('\n'))))
print('Final C pthread time:',mean(map(float,open('c_pthread.out','r').read().strip().split('\n'))))
print('Final Python serial time:',mean(map(float,open('py_serial.out','r').read().strip().split('\n'))))
print('Final Python pyMP time:',mean(map(float,open('py_pyMP.out','r').read().strip().split('\n'))))
print('Final Python multiprocessing time:',mean(map(float,open('py_multiprocessing.out','r').read().strip().split('\n'))))
