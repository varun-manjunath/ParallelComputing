import sys
import random
import pymp

r=random.Random()

if len(sys.argv)==2:
	if(sys.argv[1] in ('-s','--size')):
		try:
			arraySize=int(sys.argv[2])
		except Exception as e:
			print('Error! Please enter a valid size\nExample: python3 driver.py -s 10000\n')
			print(e.what())
			sys.exit(1)

		# Synchronized access will slow things down, one write at a time
		# testList=pymp.shared.array((arraySize,),autolock=False)

		# with pymp.Parallel(4) as p:
		# 	for i in p.range(arraySize):
		# 		testList[i]=r.randint(0,512)

		# print(testList)

		with open('comparison.h','w') as headerFile:
			headerFile.write('long array_size='+str(arraySize)+';\n')
		
		# 5 runs
		for i in range(5):
			with open('test_case','w')	
		# headerFile.write('long x[]={'+str(testList).replace('[','{').replace(']','}')+';')import sys
import os
import random
import pickle
from statistics import mean

r=random.Random()
testCaseCount=6
# 6 test cases
for i in range(1,testCaseCount+1):
	arraySize=10**i

	testList=[0]*arraySize
	arraySizeString=str(arraySize)
	commands=['gcc -g serialAddVector.c;./a.out '+arraySizeString,'python serialAddVector.py '+str(i)]
	prefix='test_case_'+str(i)+'_'
	
	with open('comparison.h','w') as headerFile:
		headerFile.write('long array_size='+str(arraySize)+';')
		headerFile.write('char x_test_case_file_name[100]="'+prefix+'x.txt'+'";')
		headerFile.write('char y_test_case_file_name[100]="'+prefix+'y.txt'+'";')
		# headerFile.write('long x[]={'+str(testList).replace('[','{').replace(']','}')+';')
	
	with open(prefix+'x'+'.txt','w') as xFile:
		for k in range(arraySize):
			temp=r.randint(0,512)
			testList[k]=temp
			xFile.write(str(temp)+'\n')

	# using testList pickling to quickly load random integers into the Python programs
	with open(prefix+'x.pkl','wb') as xPickleFile:
		pickle.dump(testList,xPickleFile)

	with open(prefix+'y.txt','w') as yFile:
		for k in range(arraySize):
			temp=r.randint(0,512)
			testList[k]=temp
			yFile.write(str(temp)+'\n')

	with open(prefix+'y.pkl','wb') as yPickleFile:
		pickle.dump(testList,yPickleFile)

	for command in commands:
		# 5 runs for each test case
		for j in range(5):
			#execute the programs
			if(j==1 and i==3): sys.exit(11)
			os.system(command)

# 6 test cases
c_serial_ouput_times=list(map(float,open('c_serial.out','r').read().strip().split('\n')))

p=0
q=7
for i in range(testCaseCount):
	print(mean(c_serial_ouput_times[p:q]))
	p+=6
	q+=6

print('C serial time:',mean(temp))
print('Python serial time:',mean(map(float,open('py_serial.out','r').read().strip().split('\n'))))
