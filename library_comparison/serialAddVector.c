#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include "comparison.h"
#include <errno.h>
#include <string.h>

extern long array_size;
extern char x_test_case_file_name[100];
extern char y_test_case_file_name[100];

int main()
{
	int* x=malloc(array_size*sizeof(int));
	int* y=malloc(array_size*sizeof(int));
	int* z=malloc(array_size*sizeof(int));

	for(long i=0;i<array_size;++i)
	{
		FILE* x_stream=fopen(x_test_case_file_name,"r+");
		FILE* y_stream=fopen(y_test_case_file_name,"r+");
	
		fscanf(x_stream,"%d",&x[i]);
		fscanf(y_stream,"%d",&y[i]);
	}

	struct timespec s;
	struct timespec e;

	clock_gettime(CLOCK_REALTIME,&s);

	for(long i=0;i<array_size;++i)
	{
		z[i]=x[i]+y[i];
	}

	clock_gettime(CLOCK_REALTIME,&e);

	double elapsedTime=((double) e.tv_sec + ((double) s.tv_nsec) * 1.0e-9) - (double) e.tv_sec + ((double) s.tv_nsec) * 1.0e-9;
	printf("Time taken: %.2lf seconds\n",elapsedTime);
	
	//O_RDWR is required, else a bad file descriptor runtime error will be thrown by dprintf
	int fd=open("c_serial.out",O_CREAT|O_RDWR|O_APPEND,0777);

	if(dprintf(fd,"%.2lf\n",elapsedTime)<0){
		printf("%s",strerror(errno));
	};
	close(fd);
	
	free(x);
	free(y);
	free(z);
	return 0;
}