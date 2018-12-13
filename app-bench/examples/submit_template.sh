#!/bin/bash -l
# -l option required so that module command works
#
#PBS -l nodes=1:ppn=40:likwid:f2.2,walltime=03:00:00
#
# job name
#PBS -N bench_campaign
#
# stdout and stderr files
#PBS -o job.out -e job.err
#
# first non-empty non-comment line ends PBS options

# Intel compiler , likwid tools
module load intel64/17.0up01 likwid/4.2.0

DATA_DIR=##DATA_DIR##
RESULTS_DIR=##RES_DIR##
EXEC=##EXEC_DIR##

cd $RESULTS_DIR

export KMP_INIT_AT_FORK=FALSE

for nthread_socket_0 in ##THREADS_LOOP##
do
    mkdir -p $RESULTS_DIR/$((nthread_socket_0 + 1))n
    echo ":: Socket 0: $((nthread_socket_0 + 1)) threads, Socket 1 0 threads CACHES"
    likwid-perfctr -C S0:0-${nthread_socket_0} -g CACHES -m -O -s 0x0 ${EXEC} -d ${DATA_DIR} -e 5.0 --binqueue --multiple ##DUP_FAC## > $RESULTS_DIR/$((nthread_socket_0 + 1))n/caches.txt
done


