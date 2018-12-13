from __future__ import print_function
import os
import shutil
import subprocess
import argparse
import sys
import re

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vect', nargs='*',default=['SSE', 'AVX'],
        help='vectorization levels (default: [SSE,AVX])')
parser.add_argument('-n', '--nthreads', nargs='*',
        default=[1,2,4,8],type=int,
        help='sequence of nthreads for benchmarks (default: [1,2,4,8])')
parser.add_argument('-r', '--runs', nargs='*',
        default=[0,1,2,3,4],type=int,
        help='sequence of runs for benchmarks (default: [0,1,2,3,4])')
parser.add_argument('-t', '--test', action='store_true',
        help='flag to test script (runs a single iteration)')
parser.add_argument('-b', '--binq', action='store_true',
        help='flag to submit the binq bench version of the executable')
parser.add_argument('-d', '--data-dir', type=str, required=True,
                help='data directory with coreneuron dataset' )
parser.add_argument('-w', '--weak-scaling', action='store_true',
            help='activates weak scaling mode (default: off)' )
parser.add_argument('-s', '--single-thread', action='store_true',
                help='only perform single thread benchmarks (default: off)')
parser.add_argument('-g', '--single-run', action='store_true',
                help='only perform a single run of the benchmarks (default: off)')
args = parser.parse_args()

#### CONFIG
# base_exec_dir and vect_2_exec are such that:
# base_exec_dir + vect_2_exec[vec] + '/bin/coreneuron_exec'
# points to the coreneuron executable
base_exec_dir='/home/hpc/ihpc/ihpc029h/soft/coreneuron/'
vect_2_exec=dict(
        SSE='install-likwid',
        AVX='install-likwid-avx-IVB',
        )
####

data_dir=args.data_dir
vect_levels=args.vect

if args.single_run:
    runs = [0]
else:
    runs = args.runs

nthreads = args.nthreads
if args.test or args.single_thread:
    nthreads = [1]
nthreads = sorted( nthreads )
nthreads.reverse()
#### END CONFIG

base_dir = os.getcwd()

for vec in vect_levels:
    base_name = data_dir.split('/')[-1] if data_dir.split('/')[-1] else data_dir.split('/')[-2]
    vec_dir_name = re.split('_[0-9]*cells.*', base_name)[0]
    vec_dir_name += '_' + vec + '_ivb'
    for run in runs:
        run_dir_name = 'run' + str(run)
        experiment_dir = os.path.join( base_dir, vec_dir_name, run_dir_name )
        if not os.path.exists(experiment_dir):
            os.makedirs( experiment_dir )
        shutil.copyfile( 'submit_template.sh', os.path.join( experiment_dir, 'submit.sh' ) )

        with open( os.path.join( experiment_dir, 'submit.sh' ), 'r' ) as submit_f:
            filedata = submit_f.read()

        filedata = filedata.replace( '##DATA_DIR##', data_dir )
        filedata = filedata.replace( '##RES_DIR##', experiment_dir )
        if not args.binq:
            filedata = filedata.replace( '##EXEC_DIR##', base_exec_dir + vect_2_exec[vec] + '/bin/coreneuron_exec' )
        else:
            filedata = filedata.replace( '##EXEC_DIR##', base_exec_dir + 'install-binq-bench/bin/coreneuron_exec' )

        if args.weak_scaling:
            filedata = filedata.replace( '##DUP_FAC##', '$((nthread_socket_0 + 1))' )
        else:
            filedata = filedata.replace( '##DUP_FAC##', str(int(max(nthreads))) )

        threads_loop_str = str()
        for nt in nthreads:
            threads_loop_str += str(int(nt-1)) + ' '
        filedata = filedata.replace( '##THREADS_LOOP##', threads_loop_str )

        with open( os.path.join( experiment_dir, 'submit.sh' ), 'w' ) as submit_f:
            submit_f.write( filedata )

        os.chdir( experiment_dir )
        for nt in nthreads:
            threads_result_dir = os.path.join( experiment_dir, str(nt) + 'n' )
            if not os.path.exists( threads_result_dir ):
                os.makedirs( threads_result_dir )
        subprocess.call( ['qsub', 'submit.sh'] )
        os.chdir( base_dir )

        if args.test:
            sys.exit(0)

