#include <algorithm>
#include <ctime>
#include <iostream>
using namespace std;

#define ARRAY_SIZE 10000

// comparator function used for C standard library quick sort
static int comparator(const void* a, const void* b)
{
	// As the parameters are supposed to be constant void pointers
	// So, explicit casts and indirections are used to get the right semantic meaning out of the variables
	// comparator function basically returns (num1-num2) to be used by qsort
	return *((int*)a)-*((int*)b);
}

int main()
{
	// allocate in stack
	// heap allocation does not make much of a difference
	int array[ARRAY_SIZE];

	//generate random array
	for(int c=0;c<ARRAY_SIZE;++c)
	{
		array[c]=rand()%512;
	}	

	// Included in algorithm header
	sort(array, array + arraySize);

	/*
		Can you see why a sorted array makes the thresholdSum much faster?
		Try reasoning it out!

		If you think you got it, verify by visiting:
			http://magical-parallel-computing.blogspot.in/2017/04/a-simple-python-program-using.html
	
		Don't worry if you don't get it either, this is very subtle...
		Just go out for a stroll in the local park, enjoy the soothing breeze and notice the chirping birds on the swaying branches...
		Just check out the weather prediction report before you do venture out...
		
		Maybe now you have a spark of inspiration from nature...
	*/

	// alternative sort function C library, not standardized as quick sort, but current implementation is quick sort.
	// qsort(array,ARRAY_SIZE,sizeof(int),comparator);

	clock_t start=clock();
	long long sum=0;

	for(int i=0;i<10000;++i)
	{
		for(int j=0;j<ARRAY_SIZE;++j)
		{
			if(array[j]>256)
			{
				sum+=array[j];
			}
		}
	}

	// calculate elapsed time
	double elapsedTime=(double)(clock()-start)/CLOCKS_PER_SEC;

	cout<<"Time taken: "<<elapsedTime<<std::endl;
	// cout<<"Sum is: "<<sum<<std::endl;
}