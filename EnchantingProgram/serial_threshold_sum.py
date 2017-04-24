'''
	If you haven't seen the C/C++ programs prior to this Python program, go have a look at those first.

	In the C and C++ examples of threshold sum, we saw a large speedup, is it so in this case? (Python)
	Why not?

	There's another influncing factor in Python, which attenuates the speedup effect due to sorting...
	Visit http://magical-parallel-computing.blogspot.in/2017/04/a-simple-python-program-using.html for details

'''

import time
import sys
import random

array=[]
r=random.Random()

# create random list for threshold sum
for i in range(10000):
	array.append(r.randint(0,512))

#make a copy of the same list to sort later
b=array.copy()
start=time.time()

s=0
for i in range(10000):
	for x in array:
		if x>256:
			s+=x
end=time.time()
print("Time taken: ",end-start)

# Sort and test
array=b
array.sort()

start=time.time()
s=0
#Python's version of threshold sum
for i in range(10000):
	for x in array:
		if x>256:
			s+=x

'''

# In Python, an intrinsic speedup of alomst 2x can be achieved just by using a Pythonic syntax
# Use generators/list comprehension instead of traditional for loops...

# list comprehension
s=sum([x for x in array if x>256])

#generators
s=sum(x for x in array if x>256)

'''

end=time.time()
print("Time taken: ",end-start)

# if required, verify correctness with unsorted sum output
# print('Sum is:',s)