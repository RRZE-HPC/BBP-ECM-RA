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

#define NREP 50000
#define NFIXEDPOINTREP 2000
#define VECSIZE 2

// ATTENTION this does not work as intended for now

int main() {

    LIKWID_MARKER_INIT;

    int i,j,k;
    double *x;
    int tmp;
    tmp = posix_memalign( (void**) &x, 64, 8*sizeof(double) );

    LIKWID_MARKER_START("loop");
    for (j=0; j<NREP; ++j) {
        x[0]=0.001;
        x[1]=0.0011;
        x[2]=0.001;
        x[3]=0.0011;
        x[4]=0.001;
        x[5]=0.0011;
        x[6]=0.001;
        x[7]=0.0011;
        for (i=0; i<NFIXEDPOINTREP; ++i){
#pragma nounroll
#pragma vector temporal
#pragma omp simd simdlen(VECSIZE)
            for( k=0; k<VECSIZE; ++k) {
                x[k] = exp(x[k]-1.);
            }
        }
    }
    LIKWID_MARKER_STOP("loop");

    printf("Finished! %f\n", x[VECSIZE-1]);
    printf("Total number of scalar iterations: %d\n", VECSIZE*NREP*NFIXEDPOINTREP);

    LIKWID_MARKER_CLOSE;

    return 0;
}
