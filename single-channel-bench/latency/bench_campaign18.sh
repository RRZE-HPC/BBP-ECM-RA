#!/bin/bash -l
# -l option required so that module command works
#
#PBS -l nodes=1:ppn=40:likwid:f2.2,walltime=05:00:00
#
# job name
#PBS -N bench_campaign
#
# stdout and stderr files
#PBS -o job.out -e job.err
#
# first non-empty non-comment line ends PBS options

module load intel64/17.0up01 likwid/4.3.2

cd /home/hpc/ihpc/ihpc029h/bench/latency/dependency-on-num-streams

for NSTREAM in 18
do
    if [ ! -d "${NSTREAM}streams" ]; then
        mkdir ${NSTREAM}streams
    fi

    NREP=500
    for SZ in 12500 125000
    do
        sed "s/##NREP##/${NREP}/g" bench.template.${NSTREAM}streams > bench.${NSTREAM}streams.c
        sed -i "s/##ARRAY_SIZE##/${SZ}/g" bench.${NSTREAM}streams.c

        icpc -std=c++11 -DLIKWID_PERFMON -O3 -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp bench.${NSTREAM}streams.c -o bench.${NSTREAM}streams $LIKWID_LIB -llikwid

        likwid-perfctr -g CACHES -m -C S0:0-0 ./bench.${NSTREAM}streams > ${NSTREAM}streams/bench.sz${SZ}.nrep${NREP}.output.txt
    done

    NREP=50
    for SZ in 1250000 5000000 50000000
    do
        sed "s/##NREP##/${NREP}/g" bench.template.${NSTREAM}streams > bench.${NSTREAM}streams.c
        sed -i "s/##ARRAY_SIZE##/${SZ}/g" bench.${NSTREAM}streams.c

        icpc -std=c++11 -DLIKWID_PERFMON -O3 -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp bench.${NSTREAM}streams.c -o bench.${NSTREAM}streams $LIKWID_LIB -llikwid

        likwid-perfctr -g CACHES -m -C S0:0-0 ./bench.${NSTREAM}streams > ${NSTREAM}streams/bench.sz${SZ}.nrep${NREP}.output.txt
    done


   NREP=25
    for SZ in 100000000 250000000
    do
        sed "s/##NREP##/${NREP}/g" bench.template.${NSTREAM}streams > bench.${NSTREAM}streams.c
        sed -i "s/##ARRAY_SIZE##/${SZ}/g" bench.${NSTREAM}streams.c

        icpc -std=c++11 -DLIKWID_PERFMON -O3 -g -qopt-report=5 -qopt-report-phase=vec -qopt-streaming-stores never -restrict $LIKWID_INC -qopenmp bench.${NSTREAM}streams.c -o bench.${NSTREAM}streams $LIKWID_LIB -llikwid

        likwid-perfctr -g CACHES -m -C S0:0-0 ./bench.${NSTREAM}streams > ${NSTREAM}streams/bench.sz${SZ}.nrep${NREP}.output.txt
    done

done
