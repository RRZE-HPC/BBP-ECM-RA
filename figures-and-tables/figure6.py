import numpy as np
import matplotlib.pyplot as plt
import argparse
import re
import os

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

def getNinstances(l):
    return np.array( [ x[1] for x in l ] )

def getNtimeIter(l):
    return [ x[2] for x in l ]

parser = argparse.ArgumentParser(description='')
parser.add_argument('--model', '-m', type=str,
            default='ecm_figures_bbp.models.L5TTPC_all_channels',
            help='name of neuron model (with full module import expansion)\
                e.g. ecm_figures_bbp.models.L5TTPC_all_channels')
parser.add_argument('--path', '-p', type=str,
        default='../results/states-and-kernels/',
        help='path to results root folder')

args = parser.parse_args()

exec( 'nrn = ' + args.model + '()' )

archs = [
        ecm_figures_bbp.ecm.IVB.SSE.socket(),
        ecm_figures_bbp.ecm.IVB.AVX.socket(),
        ecm_figures_bbp.ecm.SKX.SSE.socket(),
        ecm_figures_bbp.ecm.SKX.AVX.socket(),
        ecm_figures_bbp.ecm.SKX.AVX512.socket()
        ]
arch_marker_style = [ '^', 'v', 'D', 's', 'p']
arch_color = ['#547e2b']*2
arch_color.extend( ['#77000e']*3 )

fig, ax = plt.subplots(figsize=(8,5))

theor_max_BW = list()
for datadir in os.listdir(args.path):
    if 'tds' in datadir:
        if 'SSE' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.SSE.socket()
            arch_idx=2
        elif 'AVX512' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.AVX512.socket()
            arch_idx=4
        elif 'AVX' in datadir:
            arch = ecm_figures_bbp.ecm.SKX.AVX.socket()
            arch_idx=3
        else:
            print( 'Unrecognised architecture', datadir)
            continue
    elif 'ivb' in datadir:
        if 'SSE' in datadir:
            arch = ecm_figures_bbp.ecm.IVB.SSE.socket()
            arch_idx=0
        elif 'AVX' in datadir:
            arch = ecm_figures_bbp.ecm.IVB.AVX.socket()
            arch_idx=1
        else:
            print( 'Unrecognised architecture', datadir)
            continue
    else:
        print( 'Unrecognised architecture', datadir)
        continue

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

    data_volumes = np.zeros( shape=(len(nrn.kernels), len(nthreads), n_runs ) )
    frequencies = np.zeros( shape=(len(nrn.kernels), len(nthreads), n_runs ) ) # in Hz
    times = np.zeros( shape=(len(nrn.kernels), len(nthreads), n_runs ) )

    for irun, run in enumerate(runs):
        rundir = os.path.join(args.path, datadir, 'run' + str(run) )
        for th_idx, thread in enumerate(nthreads):
            if thread == 1:
                continue
            expdir = os.path.join(rundir, str(thread) + 'n' )
#            print( expdir )
            with open( os.path.join( expdir, 'caches.txt' ), 'r' ) as meas_f:
                lines = meas_f.readlines()

            for k_idx, k in enumerate(nrn.kernels):
#                print( k[0]['name'] )
                kname = k[0]['name'].split(' ')[0]

                if kname == 'linear':
                    continue
                elif  'spike delivery' in k[0]['name']:
                    meas_name = names2meas(k[0]['name'])
                else:
                    if kname == 'exc':
                        kname='DetAMPANMDA'
                    if kname == 'inh':
                        kname = 'DetGABAAB'
                    meas_name = names2meas(k[0]['name'])

                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw STAT,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
                #### DEBUG
                #if 'ivb' in datadir and 'SSE' in datadir and th_idx == 1 and k[0]['name'] == 'Ih current':
                #    print( float( lines[idx + idx_meas].split(',')[5] ) )

                #pos_in_line = 5 # for average
                pos_in_line = 4 # for max
                times[ k_idx, th_idx, irun ] = float( lines[idx + idx_meas].split(',')[pos_in_line] )

                idx_freq = next(i for i,v in enumerate(lines[idx:]) if 'Clock [MHz] STAT' in v)
                pos_in_line = 4 # for avg
                frequencies[ k_idx, th_idx, irun ] = float( lines[idx + idx_freq].split(',')[pos_in_line] )*1e+6
                times[ k_idx, th_idx, irun ] /= frequencies[ k_idx, th_idx, irun ]

                idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Metric STAT,CACHES' in v)

                idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'Memory data volume' in v)
                #### DEBUG
                #if 'ivb' in datadir and 'SSE' in datadir and th_idx == 1 and k[0]['name'] == 'Ih current':
                #    print( float( lines[idx + idx_meas].split(',')[5] ) )

                #pos_in_line = 5 # for average
                pos_in_line = 1 # for sum
                data_volumes[ k_idx, th_idx, irun ] = float( lines[idx + idx_meas].split(',')[pos_in_line] )

        # Handle the single thread separately
        with open( os.path.join( rundir, '1n', 'caches.txt' ), 'r' ) as meas_f:
            lines = meas_f.readlines()
        for k_idx, k in enumerate(nrn.kernels):
#                print( k[0]['name'] )
            kname = k[0]['name'].split(' ')[0]

            if kname == 'linear':
                continue
            elif  'spike delivery' in k[0]['name']:
                meas_name = names2meas(k[0]['name'])
            else:
                if kname == 'exc':
                    kname='DetAMPANMDA'
                if kname == 'inh':
                    kname = 'DetGABAAB'
                meas_name = names2meas(k[0]['name'])

            idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Raw,CACHES' in v)

            idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
            pos_in_line = 2
            times[ k_idx, 0, irun ] = float( lines[idx + idx_meas].split(',')[pos_in_line] )
            idx_freq = next(i for i,v in enumerate(lines[idx:]) if 'Clock [MHz]' in v)
            pos_in_line = 1
            frequencies[ k_idx, 0, irun ] = float( lines[idx + idx_freq].split(',')[pos_in_line] )*1e+6
            times[ k_idx, 0, irun ] /= frequencies[ k_idx, 0, irun ]

            idx = next(i for i,v in enumerate(lines) if 'TABLE,Region ' + meas_name in v and 'Metric,CACHES' in v)

            idx_meas = next(i for i,v in enumerate(lines[idx:]) if 'Memory data volume' in v)
            #### DEBUG
            #if 'ivb' in datadir and 'SSE' in datadir and th_idx == 1 and k[0]['name'] == 'Ih current':
            #    print( float( lines[idx + idx_meas].split(',')[pos_in_line] ) )

            pos_in_line = 1
            data_volumes[ k_idx, 0, irun ] = float( lines[idx + idx_meas].split(',')[pos_in_line] )

    if arch.name == 'SKX AVX512':
        for k_idx, k in enumerate(nrn.kernels):
            if 'linear algebra' in k[0]['name']:
                continue
            print( k[0]['name'],
                    100.*np.median(data_volumes[k_idx, 0, : ]/times[k_idx, 0, : ] )/arch.mem_BW )
    tot_times = np.sum( times, axis=0 ) # in s
    tot_volumes = np.sum( data_volumes, axis=0) # in GB
    measurements = tot_volumes/tot_times # in GB/s
#    measurements *= arch.cpu_f # in GB/s
    frequencies = np.mean(np.median( frequencies, axis=2 ), axis=1 )
    avg_frequency = np.sum(frequencies*np.mean(np.median(times, axis=2 ), axis=1 ))/np.sum( np.mean(np.median(times, axis=2 ), axis=1 ) )
    theor_max_BW.append( arch.mem_BW*avg_frequency/arch.cpu_f*1e-9 )

#    print( arch.name, 'frequencies', frequencies )
#    print( arch.name, 'times', np.mean(np.median(times, axis=2 ), axis=1 ) )
#    print( arch.name, avg_frequency, arch.cpu_f )
#    print( arch.name, 'theor_max_BW', theor_max_BW, arch.mem_BW )

    measurements = 100.*measurements/theor_max_BW[-1]
    median_tot_meas = np.median(measurements, axis=1)

    print( '**',arch.name,  median_tot_meas, '**')

    q25 = np.abs(
            np.quantile(measurements, 0.25, axis=1) -
            median_tot_meas )
    q75 = np.abs(
            np.quantile(measurements, 0.75, axis=1) -
            median_tot_meas )
    ax.errorbar( nthreads, median_tot_meas,
            yerr=np.vstack((q25,q75)),
            fmt=arch_marker_style[arch_idx], color=arch_color[arch_idx],
            label=arch.name, markersize=6)

#---------------------------------------------------------------------
n_instances = getNinstances( nrn.kernels )
for arch_idx, arch in enumerate(archs):
    numerator = np.zeros( shape=(len(archs), 18) )
    denominator = np.zeros( shape=(len(archs), 18) )
    percent_mem_bw = np.zeros_like( numerator )
    mem_traffic = np.zeros( shape=(len(nrn.kernels) ,) )
    for nth in range(1,int(arch.max_nthreads)+1):
        predictions = ecm_figures_bbp.ecm.predictions.runtime( arch, nrn, nth )['DRAM']
#        tot_runtime = np.sum( predictions )/arch.cpu_f # in ns
        tot_runtime = 0.
        for i,k in enumerate(nrn.kernels):
            if 'linear' in k[0]['name'] or 'delivery' in k[0]['name']:
                continue
#            numerator[arch_idx,nth-1] += arch.TMem( k[0] )
#            denominator[arch_idx,nth-1] += predictions[i]
#    percent_mem_bw = 100.*numerator/denominator

            tot_runtime += predictions[i]
            mem_traffic[i] = ecm_figures_bbp.ecm.predictions.mem_traffic( k[0] )#*n_instances[i]*1e-3
            if arch.name == 'SKX AVX512' and nth==1:
                print( 'prediction', arch.name, k[0]['name'], 100.*(mem_traffic[i]/predictions[i])/theor_max_BW[arch_idx]*frequencies[i] )
        tot_runtime /= frequencies[i]*1e-9
        tot_traffic = np.sum( mem_traffic )
        percent_mem_bw[arch_idx,nth-1] += 100.*(tot_traffic/tot_runtime)/theor_max_BW[arch_idx]

    ax.plot( range(1,int(arch.max_nthreads)+1), percent_mem_bw[arch_idx,:int(arch.max_nthreads)],
            '--', color=arch_color[arch_idx],
            label=arch.name, linewidth=1.0 )


    print( percent_mem_bw[arch_idx,:] )
ax.set_xticks(range(1,19)[::3])
ax.set_xticklabels(range(1,19)[::3])
ax.set_ylim( [0., 101.] )
ax.legend()

ax.set_ylabel('Percent of runtime in saturated regime')
ax.set_xlabel('Number of shared memory threads')

fig.savefig('percent-bw.pdf')
