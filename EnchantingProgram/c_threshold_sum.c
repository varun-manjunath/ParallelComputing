#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define ARRAY_SIZE 10000

static int cmpIntegers(const void* a, const void* b)
{
	return *((int*)a) - *((int*)b);
}

int main()
{
	//seed the random function with the current time
	srand(time(NULL));
	int* array=malloc(sizeof(int)*ARRAY_SIZE);

	for(int i=0;i<ARRAY_SIZE;++i)
	{
		array[i]=rand()%512;
	}

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

	//C (stdlib.h) standard library sort
	qsort(array,ARRAY_SIZE,sizeof(int),cmpIntegers);

	clock_t start=clock();

	long sum=0;
	// multiplicative loop
	for(int iter=0;iter<10000;++iter)
	{
		for(int i=0;i<ARRAY_SIZE;++i)
		{
			//threshold
			if(array[i]>256)
			{
				//some operation here
				sum+=array[i];
			}
		}
	}

	clock_t end=clock();
	printf("Time taken: %lf\n", (double)(end - start)/CLOCKS_PER_SEC);
	printf("Sum: %ld\n",sum);
}