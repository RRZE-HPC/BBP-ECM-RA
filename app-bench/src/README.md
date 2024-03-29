# COMPILING CORENEURON

## 1. Environment
Requires
- intel compiler 18.0.1 for SKX or 17.0.1 for IVB
- likwid 4.2.0
- cmake
- git

For example, these are the modules for the IVB emmy machine

```
$ module load intel64/17.0up01 likwid/4.2.0 cmake git
```

## 2. get source code

You need to get a specifically instrumented fork of the code

```
$ git clone --recursive https://github.com/sharkovsky/CoreNeuron.git
```

depending on which benchmark you will run, you can build the general version (also valid for single-channel benchmarks)

```
$ git checkout perf_eng_erlangen
```

OR the spike-delivery specific version

```
$ git checkout perf_eng_binq_bench
```

OR the linear algebra specific version

```
$ git checkout perf_eng_linalg
```

## 3. CMake

change the `<PREFIX>` below

```
$ CC=icc CXX=icpc cmake -DCMAKE_INSTALL_PREFIX=<PREFIX> -DADDITIONAL_MECHPATH=app-bench/src/modfiles -DADDITIONAL_MECHS=app-bench/src/modfiles/coreneuron_mechs.txt -DCMAKE_CXX_FLAGS="-O2 -g -qopt-report -qopt-report-phase=vec -qopt-streaming-stores never -restrict ${LIKWID_INC} -DLIKWID_PERFMON" -DCMAKE_C_FLAGS="-O2 -g -qopt-report -qopt-report-phase=vec -qopt-streaming-stores never -restrict ${LIKWID_INC} -DLIKWID_PERFMON" -DCMAKE_EXE_LINKER_FLAGS="${LIKWID_LIB} -llikwid" -DUNIT_TESTS=OFF  -DENABLE_NET_RECEIVE_BUFFERING=OFF ..
```

## 4. Build

it will be a bit of a convoluted process, we need to build the app once, overwrite some files (that were automatically generated during the build process) and rebuild it

#### 4.1
$ make

#### 4.2
first select a vectorization level for the build, e.g. SSE.
We need to make sure all pragma omp simdlen are set correctly, using:

```
$ ./app-bench/src/instrumented_c_files/simdify.sh app-bench/src/instrumented_c_files/ 2
```

Then we copy the files to where we need them

```
$ cp app-bench/src/instrumented_c_files/*.c <BUILD_DIR>/coreneuron/
```

OR, if you're building a version for single-channel benchmarks

first manually check that simdlen is set correctly in the *.synthetic_bench files, then copy them to where we need them

```
$ for f in  app-bench/src/instrumented_c_files/*.synthetic_bench; do cp $f <BUILD_DIR>/coreneuron/${f/.synthetic_bench/.c}; done
```

#### 4.3
$ make && make install

