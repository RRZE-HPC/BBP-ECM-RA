# COMPILING CORENEURON

## 1. Modules (on IVB emmy)

$ module load intel64/17.0up01 likwid/4.2.0 cmake git

## 2. get source code

You need to get my specially instrumented fork of the code

$ git clone --recursive https://github.com/sharkovsky/CoreNeuron.git

depending on which benchmark you will run, you can build the general version

$ git checkout perf_eng_erlangen

OR the spike-delivery specific version
$ git checkout perf_eng_binq_bench

OR the linear algebra specific version
$ git checkout perf_eng_linalg

## 3. CMake

$ CC=icc CXX=icpc cmake -DCMAKE_INSTALL_PREFIX=<PREFIX> -DADDITIONAL_MECHPATH=app-bench/src/modfiles -DADDITIONAL_MECHS=app-bench/src/modfiles/coreneuron_mechs.txt -DCMAKE_CXX_FLAGS="-O2 -g -qopt-report -qopt-report-phase=vec -qopt-streaming-stores never -restrict ${LIKWID_INC} -DLIKWID_PERFMON" -DCMAKE_C_FLAGS="-O2 -g -qopt-report -qopt-report-phase=vec -qopt-streaming-stores never -restrict ${LIKWID_INC} -DLIKWID_PERFMON" -DCMAKE_EXE_LINKER_FLAGS="${LIKWID_LIB} -llikwid" -DUNIT_TESTS=OFF  -DENABLE_NET_RECEIVE_BUFFERING=OFF ..

## 4. Build

it will be a bit of a convoluted process, we need to build the app once, overwrite some files (that were automatically generated during the build process) and rebuild it

$ make

$ cp app-bench/src/instrumented_c_files/*.c <BUILD_DIR>/coreneuron/

$ make && make install

