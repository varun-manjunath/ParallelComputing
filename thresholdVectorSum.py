import sys
import time
import random
import multiprocessing

#Compute the sum of all integers along each row with a threshold of >=50.

#Input: list of lists (rectangular matrix)(N rows,M columns) of randomized integers ranging from 0 to 100
#Output: a list of size Nx1 containing the thresholded sums

numRows=1000
numColumns=10000
results=[]
r=random.Random()

#create a shared array so that all the threads can write their results
output=multiprocessing.Array('i',(0,)*numRows,lock=False)

#traverse through lists of numbers
matrix=[[0] for x in range(numRows)]
for row in matrix:
	for i in range(numColumns):
		#Use the randint function to ditribute samples from 0 to 512
		row.append(r.randint(0,512))

#Sorting reduces time
for x in range(numRows):
	matrix[x].sort()

start=time.time()

def thresholdSum(vectorIndex):
	'''
		Return the sum of all the integers in a given row of the global matrix, beyond a given threshold
		If an element does not pass the threshold, it is not added
	'''
	sum=0
	#index into matrix and get the ith list
	for number in matrix[vectorIndex]:
		if number>256:
			sum+=number
	output[vectorIndex]=sum

#create a process pool for iniializing workers
pool=multiprocessing.Pool()

# iterate over number of rows
for i in range(numRows):
	results.append(pool.apply_async(thresholdSum, (i,)))

#get the asynchronous calls' results by claiming their return values
for processResult in results:
	#processResult.get(timeout=5)	#5 second timeout can also be specified
	
	# a get call without any parameters waits indefinitely for the asynchronous call to return
	processResult.get()

end=time.time()

print('Time taken: ',end-start)