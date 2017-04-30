// Author: Varun M
// Parallel computing library comparison 2017
// https://github.com/varun-manjunath/ParallelComputing/tree/master/library_comparison

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <pthread.h>
#include "comparison.h"

// Extern variables will get value from the header file
extern long array_size;
extern char x_test_case_file_name[100];
extern char y_test_case_file_name[100];

// Defined to pass work information to each thread from the main thread
typedef struct
{
	int* x;
	int* y;
	int* z;
	int startIndex;
	int endIndex;
}threadArgument;

void* threadWork(void* t)
{
	// Pointer to the threadArgument variable
	// Extensive use of namespaces... notice usage of startIndex in 3 scopes...
	// In structure, main and function...
	
	// create local copies for traversing using for loop
	threadArgument* temp=(threadArgument*)t;
	int* x=temp->x;
	int* y=temp->y;
	int* z=temp->z;
	int startIndex=temp->startIndex;
	int endIndex=temp->endIndex;

	// Each thread computes array sum on it's assigned block of the array
	for(int i=startIndex;i<endIndex;++i)
	{
		z[i]=x[i]+y[i];
	}
	
	/*
		// Tried to pass arguments using array instead of struct... unnecessary type casts... 

		int** indices=(int**)arguments;
		printf("Arguments: Start index: %d End index: %d\n",*((int*)(indices[1])),*((int*)(indices[2])));
	*/

	// Free the structure which is captured out of the (void* t) variable
	// Do NOT free variable x, y or z...
	free(temp);
	pthread_exit(0);
}

int main()
{
	// Declare timespec variables for timing the computation task
	struct timespec s;
	struct timespec e;

	// Allocate space for the three arrays on the heap
	int* x=malloc(array_size*sizeof(int));
	int* y=malloc(array_size*sizeof(int));
	int* z=malloc(array_size*sizeof(int));

	// Use the POSIX fopen method to return a file stream which is required by fscanf
	FILE* x_stream=fopen(x_test_case_file_name,"r+");
	FILE* y_stream=fopen(y_test_case_file_name,"r+");
		
	// Retrieve the elements of the array from the test case files
	for(long i=0;i<array_size;++i)
	{
		fscanf(x_stream,"%d",&x[i]);
		fscanf(y_stream,"%d",&y[i]);
	}

	// Fix number of threads, change this based on the computer's capability
	int numThreads=8;
	int blockSize=array_size/numThreads;
	
	// Get the starting time using the real-time primary clock
	clock_gettime(CLOCK_REALTIME,&s);
	
	// Create pthread array, the index in this array will be used as a thread ID
	pthread_t p[numThreads];

	int endIndex;
	int threadId=0;

	// Break up the array into many chunks of same size and allocate to different threads
	for(int startIndex=0;startIndex<array_size;startIndex+=blockSize)
	{
		// Decide the block size and finalize indices
		endIndex=startIndex+blockSize;

		// Allocate a structure on the heap to convey the specific chunk details for computation
		threadArgument* t=(threadArgument*)malloc(sizeof(threadArgument));
		t->x=x;
		t->y=y;
		t->z=z;
		t->startIndex=startIndex;
		t->endIndex=endIndex;

		// Create a pthread with default spawn arguments, give it the threadWork function and pass the arguments structure
		pthread_create(&(p[threadId]),NULL,threadWork,t);

		// Keep track of the threads to join later...
		++threadId;
	}

	// Wait for all threads to terminate and join to continue program
	// Ideally all threads finish at around the same time, in this case, it does as each thread does same amound of work
	for(int i=0;i<numThreads;++i)
	{
		pthread_join(p[i],NULL);
	}

	// Get the ending time and store into structure e
	clock_gettime(CLOCK_REALTIME,&e);

	//find the elapsed time, using timespec's second and nanosecond structure members
	double elapsedTime=((double)e.tv_sec + 1.0e-9*e.tv_nsec) - ((double)s.tv_sec + 1.0e-9*s.tv_nsec);
	printf("%ld C pthread time: %lf seconds\n",array_size,elapsedTime);
	
	//O_RDWR is required, else a bad file descriptor runtime error will be thrown by dprintf
	// Log timing information to an out file
	int fd=open("c_pthread.out",O_CREAT|O_RDWR|O_APPEND,0777);

	// display write errors, if any
	if(dprintf(fd,"%lf\n",elapsedTime)<0){
		printf("%s",strerror(errno));
	};
	close(fd);
	
	// deallocate the acquired space on the heap, else memory leak...
	free(x);
	free(y);
	free(z);
	return 0;
}
