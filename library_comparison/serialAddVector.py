import sys
import time
import pickle

test_case_num=int(sys.argv[1])

x=pickle.load(open('test_case_'+str(test_case_num)+'_x.pkl','rb'))
y=pickle.load(open('test_case_'+str(test_case_num)+'_y.pkl','rb'))
size=len(x)
z=[0]*size

before=time.time()

for i in range(0,size):
	z[i]=x[i]+y[i]
	
after=time.time()

#print(z)
timeElapsed=after-before
with open('py_serial.out','a') as outFile:
	outFile.write(str(timeElapsed)+'\n')

print('Python serial time:',timeElapsed,'seconds')
