import pickle
import argparse
import numpy as np
import matplotlib
import re
import os
import copy

font = { 'size'   : 16 }
matplotlib.rc('font', **font)

import matplotlib.pyplot as plt

arch_to_markers = {
        'ivb SSE': '^',
        'ivb AVX': 'v',
        'tds SSE': 'D',
        'tds AVX': 's',
        'tds AVX512': 'p'}

import ecm_figures_bbp

def names2meas(kname):
    if 'exc syn' in kname:
        return 'DetAMPANMDA_EMS_'+kname.split(' ')[2]
    elif 'inh syn' in kname:
        return 'DetGABAAB_EMS_'+kname.split(' ')[2]
    elif 'delivery' in kname:
        return 'DetAMPANMDA_EMS_net_receive'
    else:
        return kname.replace(' ','_')

parser = argparse.ArgumentParser(description='')
parser.add_argument('--path', '-p', type=str,
        default='../results/states-and-kernels/',
        help='path to results root folder')
parser.add_argument('--model', '-m', type=str,
        default='ecm_figures_bbp.models.L5TTPC_all_channels',
        help='name of neuron model (with full module import expansion)\
        e.g. ecm_figures_bbp.models.L5TTPC_all_channels')

args = parser.parse_args()

exec( 'nrn = ' + args.model + '()' )

whole_neuron_times_singleth = list()
whole_neuron_times_maxth = list()
architectures= list()

totfig,totax = plt.subplots()

for datadir in os.listdir(args.path):
    if 'tds' in datadir:
        if 'SSE' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.SSE.socket()
        elif 'AVX512' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.AVX512.socket()
        elif 'AVX' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.AVX.socket()
        else:
            print( 'Unrecognised architecture', datadir)
            continue
    elif 'ivb' in datadir:
        if 'SSE' in datadir:
            arch = ecm_figures_bbp.ecm.IVB.SSE.socket()
        elif 'AVX' in datadir:
            arch = ecm_figures_bbp.ecm.IVB.AVX.socket()
        else:
            print( 'Unrecognised architecture', datadir)
            continue
    else:
        print( 'Unrecognised architecture', datadir)
        continue

    architectures .append( arch )

    print( '---------------------------------------------------------')
    print( arch.name )
    print( '---------------------------------------------------------')

    if 'Hz' in datadir:
        f = float(datadir.split('Hz')[0].split('_')[-1])
    else:
        f = None

    #print( datadir )

    expdir = os.path.join(args.path, datadir )
    runs = list()
    for subdir in os.listdir( expdir ):
        if re.match( '^run[0-9]*$', subdir ) is not None:
            runs.append( int( subdir.split('run')[1] ) )
    runs = sorted( runs )
    n_runs = len(runs)

    run = runs[0]
    expdir = os.path.join(args.path, datadir, 'run' + str(run) )
    nthreads = list()
    for subdir in os.listdir( expdir ):
        if re.match( '^[0-9]*n', subdir ) is not None:
            nthreads.append( int( subdir.split('n')[0] ) )
    nthreads = sorted( nthreads )

    measurements = np.zeros( shape=(len(nrn.kernels), len(nthreads), n_runs ) )
    scaling = np.zeros_like( measurements )
    totals = np.zeros( shape=( len(nthreads), n_runs ) )
    tot_scaling = np.zeros_like( totals )
    ninstances = dict()

    for irun, run in enumerate(runs):
        print(run)
        rundir = os.path.join(args.path, datadir, 'run' + str(run) )
        for th_idx, thread in enumerate(nthreads):
            if thread == 1:
                continue
            expdir = os.path.join(rundir, str(thread) + 'n' )
#            print( expdir )
            with open( os.path.join( expdir, 'caches.txt' ), 'r' ) as meas_f:
                lines = meas_f.readlines()

            ncells = float( next( v for v in lines if 'Number of cells' in v).split(':')[1] )
            tstop = float( next( v for v in lines if 'tstop = ' in v).split('tstop = ')[1])
            nmultiples = float( next( v for v in lines if 'multiple = ' in v).split('multiple = ')[1])

            for k_idx, k in enumerate(nrn.kernels):
#                print( k[0]['name'] )
                kname = k[0]['name'].split(' ')[0]

                if kname == 'linear':
                    n_instances = float( next( v for v in lines if 'Number of compartments' in v).split(':')[1] ) # Number of compartments already includes multiples
                    meas_name = 'linalg'
                elif  'spike delivery' in k[0]['name']:
                    n_synapses = float( next(v for v in lines if 'membfunc=DetAMPANMDA' in v).split(' ')[1].split('=')[1] )*nmultiples
                    n_instances = (f*1e-3*tstop - 1.)*n_synapses
                    n_instances *= nrn.dt/tstop # this is just to counter
                    meas_name = names2meas(k[0]['name'])
                    #print(  thread, k[0]['name'], n_synapses, n_instances, meas_name )
                else:
                    if kname == 'exc':
                        kname='DetAMPANMDA'
                    if kname == 'inh':
                        kname = 'DetGABAAB'
                    try:
                        n_instances = float( next(v for v in lines if 'membfunc='+kname in v).split(' ')[1].split('=')[1] )*nmultiples
                    except StopIteration:
                        #print ( kname, 'not found' )
                        continue
                    meas_name = names2meas(k[0]['name'])

                ninstances[k[0]['name']] = n_instances
#                print( n_instances )

                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw STAT,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                ## NB taking max instead of average
                measurements[ k_idx, th_idx, irun ] = float( lines[idx + idx_meas].split(',')[4] )/( n_instances*tstop/nrn.dt )
                totals[ th_idx, irun ] += float( lines[idx + idx_meas].split(',')[4] )

        # Handle the single thread separately
        with open( os.path.join( rundir, '1n', 'caches.txt' ), 'r' ) as meas_f:
            lines = meas_f.readlines()
        for k_idx, k in enumerate(nrn.kernels):
#                print( k[0]['name'] )
            kname = k[0]['name'].split(' ')[0]

            if kname == 'linear':
                n_instances = float( next( v for v in lines if 'Number of compartments' in v).split(':')[1] )
#                print( next( v for v in lines if 'Number of compartments' in v) )
                meas_name = 'linalg'
            elif  'spike delivery' in k[0]['name']:
                n_synapses = float( next(v for v in lines if 'membfunc=DetAMPANMDA' in v).split(' ')[1].split('=')[1] )*nmultiples
                n_instances = (f*1e-3*tstop - 1.)*n_synapses
                n_instances *= nrn.dt/tstop # this is just to counter
                meas_name = names2meas(k[0]['name'])
                #print(  thread, k[0]['name'], n_synapses, n_instances, meas_name )
            else:
                if kname == 'exc':
                    kname='DetAMPANMDA'
                if kname == 'inh':
                    kname = 'DetGABAAB'
                try:
                    n_instances = float( next(v for v in lines if 'membfunc='+kname in v).split(' ')[1].split('=')[1] )*nmultiples
                except StopIteration:
                    #print ( kname, 'not found' )
                    continue
                meas_name = names2meas(k[0]['name'])

#                print( n_instances_per_cell )

            idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw,CACHES' in v)

            idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
            measurements[ k_idx, 0, irun ] = float( lines[idx + idx_meas].split(',')[2] )/( n_instances*tstop/(nrn.dt) )
            totals[ 0, irun ] += float( lines[idx + idx_meas].split(',')[2] )

#            if meas_name == 'linalg':
#                print('-- 1 threads -- run', run)
#                print( k[0]['name'], n_instances,
#                        lines[idx],
#                        lines[idx + idx_meas],
#                        lines[idx + idx_meas].split(',')[2], sep='\n' )

    for ith, th in enumerate(nthreads):
        for irun, run in enumerate(runs):
            tot_scaling[ith,irun] = totals[0,irun]/(th*totals[ith,irun])
            for k_idx in range(measurements.shape[0]):
                scaling[k_idx,ith,irun] = measurements[ k_idx, 0, irun ]/(th*measurements[ k_idx, ith, irun ])

    for ith, th in enumerate(nthreads):
        print( th, '::', tot_scaling[ith,:] )

    mean_pred = np.mean( measurements, axis=2)
    sd_pred = np.std( measurements, axis=2)
    sd_perf = np.std( 1./measurements, axis=2)

    mean_scaling = np.mean( scaling, axis=2 )
    sd_scaling = np.std( scaling, axis=2 )

    mean_tot_scaling = np.mean( tot_scaling, axis=1 )
    sd_tot_scaling = np.std( tot_scaling, axis=1 )
    median_tot_scaling = np.median( tot_scaling, axis=1 )
    q25_tot_scaling = np.quantile( tot_scaling, 0.25, axis=1 )
    q75_tot_scaling = np.quantile( tot_scaling, 0.75, axis=1 )
    max_tot_scaling = np.max( tot_scaling, axis=1 )
    min_tot_scaling = np.min( tot_scaling, axis=1 )

    predictions = np.zeros( shape=(len(nrn.kernels), len(nthreads) ) )
    for th_idx, thread in enumerate(nthreads):
        predictions[:, th_idx] = np.array(
                ecm_figures_bbp.ecm.predictions.runtime(
                    arch, nrn, nthread=thread)['DRAM'] )

    for fct in ['current', 'state']:
        fig,ax = plt.subplots()
        for i in range(predictions.shape[0]):
            if fct not in nrn.kernels[i][0]['name']:
                continue

            scaling_factor = arch.cpu_f
            p = ax.errorbar( nthreads, mean_scaling[i,:],
                    yerr = sd_scaling[i,:], fmt='-o',
                    label=nrn.kernels[i][0]['name'],
                    markersize=8 )

        ax.grid(True, which='both')
        ax.set_ylabel('Scaling efficiency')
        ax.set_xlabel('Shared memory threads')
        ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.01))
        fig.subplots_adjust( right=0.6, bottom=0.2 )
        #fig.savefig('scaling_'+ arch.name.replace(' ','_') + '_' + fct + '.pdf')

    color = '#3ebc57' if 'ivb' in datadir else '#b436c8'
    arch_name = 'ivb' if 'ivb' in datadir else 'tds'
    vect_name = 'SSE' if 'SSE' in datadir else 'AVX512' if 'AVX512' in datadir else 'AVX'
    marker = arch_to_markers[arch_name + ' '+ vect_name]
    totax.errorbar( nthreads, median_tot_scaling,
                yerr = np.vstack( (np.abs(q25_tot_scaling - median_tot_scaling),
                                   np.abs(q75_tot_scaling - median_tot_scaling))),
                fmt= '-' + marker,
                markersize=8, color=color  )

totax.grid(True, which='both')
totax.set_ylabel('Scaling efficiency')
totax.set_xlabel('Shared memory threads')
totax.set_ylim(ymin=0.)
totax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.01))
totfig.subplots_adjust( right=0.6, bottom=0.2 )
totfig.savefig('figure2_scaling_total.pdf')
