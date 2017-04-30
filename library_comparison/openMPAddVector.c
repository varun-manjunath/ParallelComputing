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
#include <omp.h>
#include "comparison.h"

// Extern variables will get value from the header file
extern long array_size;
extern char x_test_case_file_name[100];
extern char y_test_case_file_name[100];

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

	// Get the starting time using the realtime primary clock
	clock_gettime(CLOCK_REALTIME,&s);

	// Invoke openMP's parallel for to use the data parallelism potential of array addition, use 16 threads
	#pragma omp parallel for num_threads(16)
	for(long i=0;i<array_size;++i)
	{
		z[i]=x[i]+y[i];
	}

	// Get the ending time and store into structure e
	clock_gettime(CLOCK_REALTIME,&e);

	//find the elapsed time, using timespec's second and nanosecond structure members
	double elapsedTime=((double)e.tv_sec + 1.0e-9*e.tv_nsec) - ((double)s.tv_sec + 1.0e-9*s.tv_nsec);
	printf("%ld C openMP time: %lf seconds\n",array_size,elapsedTime);
	
	//O_RDWR is required, else a bad file descriptor runtime error will be thrown by dprintf
	// Log timing information to an out file
	int fd=open("c_openMP.out",O_CREAT|O_RDWR|O_APPEND,0777);

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