#include <stdio.h>
#include <stdlib.h>

// This block enables compilation of the code with and without LIKWID in place
#ifdef LIKWID_PERFMON
#include <likwid.h>
#else
#define LIKWID_MARKER_INIT
#define LIKWID_MARKER_THREADINIT
#define LIKWID_MARKER_SWITCH
#define LIKWID_MARKER_REGISTER(regionTag)
#define LIKWID_MARKER_START(regionTag)
#define LIKWID_MARKER_STOP(regionTag)
#define LIKWID_MARKER_CLOSE
#define LIKWID_MARKER_GET(regionTag, nevents, events, time, count)
#endif

#define ARRAY_SIZE 500
#define NREP 100000

int main() {

    LIKWID_MARKER_INIT;

    double * a,*b,*c;
    int tmp;
    tmp = posix_memalign( (void**) &a, 64, ARRAY_SIZE*sizeof(double) );
    tmp = posix_memalign( (void**) &b, 64, ARRAY_SIZE*sizeof(double) );

    int i,j;
    for (i=ARRAY_SIZE-1; i>=0; --i){
        a[i] = (double)i/ARRAY_SIZE;
    }

    LIKWID_MARKER_START("loop");
    for (j=0; j<NREP; ++j) {
//#pragma nounroll
#pragma vector aligned
#pragma vector temporal
#pragma omp simd simdlen(2)
        for (i=0; i<ARRAY_SIZE; ++i){
            b[i] = exp(a[i]);
        }
    }
    LIKWID_MARKER_STOP("loop");

    printf("Finished! %f\n", b[42]);
    unsigned long tot_scalar_iterations = NREP*ARRAY_SIZE;
    printf("Array Size: %d Nrep: %d i.e. Tot Scalar Iterations: %lu\n", ARRAY_SIZE, NREP, tot_scalar_iterations);

    LIKWID_MARKER_CLOSE;

    return 0;
}
