#! /bin/bash

module load intel64/17.0up01 likwid/4.3.2

## EXP THROUGHPUT - SCALAR
sed -i 's/simdlen([0-9])/simdlen(1)/g' bench_exp.c
icc -O3 -g -qopt-streaming-stores never -restrict -qopenmp -S -c bench_exp.c -o bench_exp.scalar.s
icc -DLIKWID_PERFMON -O3 -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp bench_exp.c -o bench_exp.scalar $LIKWID_LIB -llikwid
likwid-perfctr -g MEM_DP -m -C S0:0-0 ./bench_exp.scalar > bench_exp.scalar.output.txt

## EXP THROUGHPUT - SSE
sed -i 's/simdlen([0-9])/simdlen(2)/g' bench_exp.c
icc -O3 -xSSE4.2 -g -qopt-streaming-stores never -restrict -qopenmp -S -c bench_exp.c -o bench_exp.sse.s
icc -DLIKWID_PERFMON -O3 -xSSE4.2 -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp bench_exp.c -o bench_exp.sse $LIKWID_LIB -llikwid
likwid-perfctr -g MEM_DP -m -C S0:0-0 ./bench_exp.sse > bench_exp.sse.output.txt

## EXP THROUGHPUT - AVX
sed -i 's/simdlen([0-9])/simdlen(4)/g' bench_exp.c
icc -O3 -xAVX -g -qopt-streaming-stores never -restrict -qopenmp -S -c bench_exp.c -o bench_exp.avx.s
icc -DLIKWID_PERFMON -O3 -xAVX -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp bench_exp.c -o bench_exp.avx $LIKWID_LIB -llikwid
likwid-perfctr -g MEM_DP -m -C S0:0-0 ./bench_exp.avx > bench_exp.avx.output.txt

## EXP LATENCY - SCALAR
icc -O3 -g -qopt-streaming-stores never -restrict -qopenmp -S -c bench_exp_fixed_point.c -o bench_exp_fixed_point.scalar.s
icc -DLIKWID_PERFMON -O3 -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp bench_exp_fixed_point.c -o bench_exp_fixed_point.scalar $LIKWID_LIB -llikwid
likwid-perfctr -g MEM_DP -m -C S0:0-0 ./bench_exp_fixed_point.scalar > bench_exp_fixed_point.scalar.output.txt

## EXP LATENCY - SSE
sed -i 's/define VECSIZE [0-9]/define VECSIZE 2/g' bench_exp_fixed_point.vector.c
icc -O3 -xSSE4.2 -g -qopt-streaming-stores never -restrict -qopenmp -DLIKWID_PERFMON $LIKWID_INC -S -c bench_exp_fixed_point.vector.c -o bench_exp_fixed_point.vector.sse.s
icc  -DLIKWID_PERFMON -O3 -xSSE4.2 -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp  bench_exp_fixed_point.vector.c -o bench_exp_fixed_point.vector.sse $LIKWID_LIB -llikwid
likwid-perfctr -g MEM_DP -m -C S0:0-0 ./bench_exp_fixed_point.vector.sse > bench_exp_fixed_point.vector.sse.output.txt

## EXP LATENCY - AVX
sed -i 's/define VECSIZE [0-9]/define VECSIZE 4/g' bench_exp_fixed_point.vector.c
icc -O3 -xAVX -g -qopt-streaming-stores never -restrict -qopenmp -S -c bench_exp_fixed_point.vector.c -o bench_exp_fixed_point.vector.avx.s
icc  -DLIKWID_PERFMON -O3 -xAVX -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp  bench_exp_fixed_point.vector.c -o bench_exp_fixed_point.vector.avx $LIKWID_LIB -llikwid
likwid-perfctr -g MEM_DP -m -C S0:0-0 ./bench_exp_fixed_point.vector.avx > bench_exp_fixed_point.vector.avx.output.txt
