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

#define NREP 100000
#define NFIXEDPOINTREP 500

int main() {

    LIKWID_MARKER_INIT;

    int i,j;
    double x;

    LIKWID_MARKER_START("loop");
    for (j=0; j<NREP; ++j) {
        x=0.001;
#pragma nounroll
#pragma omp simd simdlen(1)
//#pragma novector
        for (i=0; i<NFIXEDPOINTREP; ++i){
            x = exp(x-1.);
        }
    }
    LIKWID_MARKER_STOP("loop");

    printf("Finished! %f\n", x);
    printf("Total number of scalar iterations: %d\n", NREP*NFIXEDPOINTREP);

    LIKWID_MARKER_CLOSE;

    return 0;
}
