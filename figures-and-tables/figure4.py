import argparse
import numpy as np
import re
import os
import tabulate

import matplotlib
font = { 'size'   : 16 }
matplotlib.rc('font', **font)

import matplotlib.pyplot as plt

import ecm_figures_bbp

parser = argparse.ArgumentParser(description='')
parser.add_argument('--path', '-p', type=str,
        default='../results/linalg/',
        help='path to results root folder')
parser.add_argument('--model', '-m', type=str,
        default='ecm_figures_bbp.models.L5TTPC_all_channels',
        help='name of neuron model (with full module import expansion)\
        e.g. ecm_figures_bbp.models.L5TTPC_all_channels')

args = parser.parse_args()

exec( 'nrn = ' + args.model + '()' )

architectures= list()

fig,ax = plt.subplots(1,1,figsize=(9,6))

for datadir in os.listdir(args.path):
    if 'AVX' not in datadir:
        continue
    if 'tds' in datadir:
        if 'SSE' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.SSE.socket()
        elif 'AVX512' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.AVX512.socket()
        elif 'AVX' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.AVX.socket()
        else:
            print( 'Unrecognised architecture', datadir)
            break
    elif 'ivb' in datadir:
        if 'SSE' in datadir:
            arch = ecm_figures_bbp.ecm.IVB.SSE.socket()
        elif 'AVX' in datadir:
            arch = ecm_figures_bbp.ecm.IVB.AVX.socket()
        else:
            print( 'Unrecognised architecture', datadir)
            break
    else:
        print( 'Unrecognised architecture', datadir)
        break

    architectures .append( arch )

    print( '---------------------------------------------------------')
    print( arch.name )
    print( '---------------------------------------------------------')

    if 'Hz' in datadir:
        f = float(datadir.split('Hz')[0].split('_')[-1])
    else:
        f = None

    print( datadir )

    expdir = os.path.join(args.path, datadir )
    #runs = ['no-permute', 'with-permute']
    runs = ['with-permute']
    n_runs = len(runs)

    run = runs[0]
    expdir = os.path.join(args.path, datadir, run )
    nthreads = list()
    for subdir in os.listdir( expdir ):
        if re.match( '^[0-9]*n', subdir ) is not None:
            nthreads.append( int( subdir.split('n')[0] ) )
    nthreads = sorted( nthreads )

    measurements = np.zeros( shape=(1, len(nthreads), n_runs ) )
    ninstances = dict()

    for irun, run in enumerate(runs):
        rundir = os.path.join(args.path, datadir, run )
        for th_idx, thread in enumerate(nthreads):
            if thread == 1:
                continue
            expdir = os.path.join(rundir, str(thread) + 'n' )
            with open( os.path.join( expdir, 'caches.txt' ), 'r' ) as meas_f:
                lines = meas_f.readlines()

            ncells = float( next( v for v in lines if 'Number of cells' in v).split(':')[1] )
            tstop = float( next( v for v in lines if 'tstop = ' in v).split('tstop = ')[1])
            nmultiples = float( next( v for v in lines if 'multiple = ' in v).split('multiple = ')[1])

            kname = 'linear'
            n_instances = float( next( v for v in lines if 'Number of compartments' in v).split(':')[1] ) # Number of compartments already includes multiples
            try:
                meas_name = 'linalg_triang'
                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw STAT,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                measurements[ 0, th_idx, irun ] = float( lines[idx + idx_meas].split(',')[5] )/( n_instances*tstop/nrn.dt )
                meas_name = 'linalg_bksub'
                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw STAT,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                measurements[ 0, th_idx, irun ] += float( lines[idx + idx_meas].split(',')[5] )/( n_instances*tstop/nrn.dt )
            except StopIteration:
                meas_name = 'linalg'
                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw STAT,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                measurements[ 0, th_idx, irun ] = float( lines[idx + idx_meas].split(',')[5] )/( n_instances*tstop/nrn.dt )

        # Handle the single thread separately
        with open( os.path.join( rundir, '1n', 'caches.txt' ), 'r' ) as meas_f:
            lines = meas_f.readlines()
            kname = 'linear'
            n_instances = float( next( v for v in lines if 'Number of compartments' in v).split(':')[1] )
            try:
                meas_name = 'linalg_triang'
                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                measurements[ 0, 0, irun ] = float( lines[idx + idx_meas].split(',')[-1] )/( n_instances*tstop/nrn.dt )
                meas_name = 'linalg_bksub'
                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                measurements[ 0, 0, irun ] += float( lines[idx + idx_meas].split(',')[-1] )/( n_instances*tstop/nrn.dt )
            except StopIteration:
                meas_name = 'linalg'
                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                measurements[ 0, 0, irun ] = float( lines[idx + idx_meas].split(',')[-1] )/( n_instances*tstop/nrn.dt )
#                print( next( v for v in lines if 'Number of compartments' in v) )


        for lin_alg_idx in range(len(nrn.kernels)):
            if 'linear' in nrn.kernels[lin_alg_idx][0]['name']:
                break

        if run == 'with-permute':
            nrn.kernels[lin_alg_idx][0]['reads'] = 4 + 2*0.5
            nrn.kernels[lin_alg_idx][0]['writes'] = 3
            nrn.kernels[lin_alg_idx][0]['CP_bound'] = False
        else:
            nrn.kernels[lin_alg_idx][0]['reads']  = 6.45
            nrn.kernels[lin_alg_idx][0]['writes'] = 4.45
            nrn.kernels[lin_alg_idx][0]['CP_bound'] = True


        predictions = np.zeros( shape=(len(nrn.kernels), len(nthreads) ) )
        for th_idx, thread in enumerate(nthreads):
            predictions[:, th_idx] = np.array(
                    ecm_figures_bbp.ecm.predictions.runtime(
                        arch, nrn, nthread=thread)['DRAM'] )

        for i in range(predictions.shape[0]):
            if 'linear' not in nrn.kernels[i][0]['name']:
                continue
            color = '#3ebc57' if 'IVB' in arch.name else '#b436c8'
            marker = 'v' if 'IVB' in arch.name else 'p'
            fill_style = 'none' if run == 'no-permute' else 'full'
            line_style = '-.' if run == 'no-permute' else '--'
            scaling_factor = arch.cpu_f

            ax.plot( nthreads, scaling_factor/measurements[0,:,irun], marker, fillstyle = fill_style, markersize=10, color=color )
            #print( run )
            #print( predictions[i,:] )
            ax.plot( nthreads, scaling_factor/predictions[i,:], line_style, color=color, linewidth=2.5, markersize=6, fillstyle=fill_style, label=arch.name.split()[0] + ' ' + run)
        #print( ecm_figures_bbp.ecm.predictions.saturation( arch, nrn ) )
        print( run )
        #print( ecm_figures_bbp.ecm.predictions.runtime(arch, nrn, nthread=1.) )
    print( np.median(measurements[0,0,:]) )
    print( np.abs( np.quantile(measurements[0,0,:], 0.75) - np.quantile(measurements[0,0,:], 0.25) ) )

ax.grid(which='both')
ax.grid(which='both')
ax.legend()
#ax.set_title(nrn.name )
ax.set_ylabel('Performance [Billion instances per second]')
ax.set_xlabel('Shared memory threads')

ax.set_ylim([0.,1.2])
ax.set_xlim([0.,17.])

fig.subplots_adjust( right=0.6, bottom=0.2 )
fig.savefig('validate-bench_linalg.pdf')
