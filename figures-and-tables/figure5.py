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
        default='../results/spike-delivery/best-case',
        help='path to directory with measurements (default: ../results/spike-delivery/best-case)')

args = parser.parse_args()

firing_interval = 0.025

map_2_n_act_per_step = {
        '4000Hz 549866syns': 4000.,
        '4000Hz 6133syns': 200.,
        '4000Hz 2173syns': 100.,
        '4000Hz 270syns': 25.,
        '4000Hz 68syns': 10.,
        '20000Hz 109973syns': 4000.,
        '20000Hz 38880syns': 2000.,
        '20000Hz 434syns': 100.,
        '20000Hz 153syns': 50.,
        '20000Hz 54syns': 25.,
        '8000Hz 97200syns': 2000.,
        '8000Hz 135syns': 25.,
        '2000Hz 73syns': 100.}

result_values = list()
# FORMAT of result_values:
# result_values[i] = [ arch_identifier, kernel identifier, nsyn_active_per_step, runtime per iteration, memory per iteration ]

for expdir in os.listdir(args.path):
    if 'spk' not in expdir:
        continue

    print( expdir )

    if 'tds' in expdir:
        arch_identifier = 0
    elif 'ivb' in expdir:
        arch_identifier = 1
    else:
        print( 'Error: Unrecognized architecture ', expdir)
        break

    runs = list()

    for subdir in os.listdir( os.path.join(args.path, expdir)):
        if re.match( '^run[0-9]*', subdir ) is not None:
            runs.append( int( subdir.split('run')[1] ) )
        runs = sorted( runs )

    kernel_identifier = 0

    for irun, run in enumerate(runs):
        rundir = os.path.join(args.path, expdir, 'run' + str(run) )
        print( rundir )

        nthreads = list()
        for threaddir in os.listdir( rundir ):
            if re.match( '^[0-9]+n', threaddir ) is not None:
                nthreads.append( int( threaddir.split('n')[0] ) )
        nthreads = sorted( nthreads )

        threaddir = os.path.join(rundir, '1n' )

        with open( os.path.join( threaddir, 'caches.txt' ), 'r' ) as meas_f:
            lines = meas_f.readlines()

        try:
            nsyn_active_per_step = float( next( v for v in lines if 'syns_active_per_step' in v).split('/')[-2].split('_')[-4].split('s')[-3] )
        except StopIteration:
            try:
                line = next( v for v in lines if 'syns_per' in v).split('/')[-2]
                key = line.split('_')[-4] + ' ' + line.split('_')[-3]
                nsyn_active_per_step = map_2_n_act_per_step[key]
            except IndexError:
                print( 'IndexError: Attempting to automatically fix' )
                line = next( v for v in lines if 'syns_per' in v).split('/')[-3]
                key = line.split('_')[-4] + ' ' + line.split('_')[-3]
                nsyn_active_per_step = map_2_n_act_per_step[key]
        except IndexError:
                print( 'IndexError: Attempting to automatically fix' )
                nsyn_active_per_step = float( next( v for v in lines if 'syns_active_per_step' in v).split('/')[-3].split('_')[-4].split('s')[-3] )

        nmultiples = float( next( v for v in lines if 'multiple = ' in v).split('multiple = ')[1])
        nsyn_active_per_step *= nmultiples

        tstop = float( next( v for v in lines if 'tstop = ' in v).split('tstop = ')[1])

        base_idx = next(i for i,v in enumerate(lines) if 'binq_delivery' in v )

#        call_count_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'call count' in v)
#        call_count = float( lines[base_idx + call_count_offset].split(',')[-2] )
        call_count = tstop/firing_interval-1.

        runtime_idx_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
        runtime = float( lines[base_idx + runtime_idx_offset].split(',')[-1] )

        mem_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'Memory data volume' in v)
        mem = 1e+9*float( lines[base_idx + mem_offset].split(',')[-2] )

        #mem_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'L2 to/from L3 data volume' in v)
        #mem = 1e+9*float( lines[base_idx + mem_offset].split(',')[-2] )

        #mem_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'L1 to/from L2 data volume' in v)
        #mem = 1e+9*float( lines[base_idx + mem_offset].split(',')[-2] )

        result_values.append(
                [ arch_identifier, 1, nsyn_active_per_step,
                    runtime/(call_count*nsyn_active_per_step),
                    mem/(call_count*nsyn_active_per_step) ]
                )

        for nthread in nthreads[1:]:
            threaddir = os.path.join(rundir, str(nthread) + 'n' )

            with open( os.path.join( threaddir, 'caches.txt' ), 'r' ) as meas_f:
                lines = meas_f.readlines()

            try:
                nsyn_active_per_step = float( next( v for v in lines if 'syns_active_per_step' in v).split('/')[-2].split('_')[-4].split('s')[-3] )
            except StopIteration:
                try:
                    line = next( v for v in lines if 'syns_per' in v).split('/')[-2]
                    key = line.split('_')[-4] + ' ' + line.split('_')[-3]
                    nsyn_active_per_step = map_2_n_act_per_step[key]
                except IndexError:
                    print( 'IndexError: Attempting to automatically fix' )
                    line = next( v for v in lines if 'syns_per' in v).split('/')[-3]
                    key = line.split('_')[-4] + ' ' + line.split('_')[-3]
                    nsyn_active_per_step = map_2_n_act_per_step[key]
            except IndexError:
                    print( 'IndexError: Attempting to automatically fix' )
                    nsyn_active_per_step = float( next( v for v in lines if 'syns_active_per_step' in v).split('/')[-3].split('_')[-4].split('s')[-3] )

            nmultiples = float( next( v for v in lines if 'multiple = ' in v).split('multiple = ')[1])
            nsyn_active_per_step *= nmultiples

            base_idx = next(i for i,v in enumerate(lines) if 'binq_delivery,Group 1 Raw' in v )

            tstop = float( next( v for v in lines if 'tstop = ' in v).split('tstop = ')[1])

            #call_count_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'call count' in v)
            #call_count = float( lines[base_idx + call_count_offset].split(',')[1] )
#            call_count = call_count/float(nthread)
            call_count = tstop/firing_interval-1.


            base_idx = next(i for i,v in enumerate(lines) if 'binq_delivery,Group 1 Raw STAT' in v )
            runtime_idx_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'CPU_CLK_UNHALTED_CORE' in v)
            #runtime = float( lines[base_idx + runtime_idx_offset].split(',')[5] )
            runtime = float( lines[base_idx + runtime_idx_offset].split(',')[4] )

            base_idx = next(i for i,v in enumerate(lines) if 'binq_delivery,Group 1 Metric STAT' in v )
            mem_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'Memory data volume' in v)
            mem = 1e+9*float( lines[base_idx + mem_offset].split(',')[1] )

            #mem_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'L2 to/from L3 data volume' in v)
            #mem = 1e+9*float( lines[base_idx + mem_offset].split(',')[1] )

            #mem_offset = next(i for i,v in enumerate(lines[base_idx:]) if 'L1 to/from L2 data volume' in v)
            #mem = 1e+9*float( lines[base_idx + mem_offset].split(',')[1] )

#            print( nthread, 'threads', call_count, 'calls', nsyn_active_per_step, 'active')

            result_values.append(
                    [ arch_identifier, nthread, nsyn_active_per_step,
                        runtime/(call_count*nsyn_active_per_step),
                        mem/(call_count*nsyn_active_per_step) ]
                    )

result_values = np.array(result_values)
print( result_values.shape )

arch_colors = ['#77000e', '#547e2b']

k = 'AMPA'
k_idx = 0

fig, ax = plt.subplots(2,1, figsize=(9,10))
barfig, barax = plt.subplots()

for arch_idx, arch in enumerate([ecm_figures_bbp.ecm.SKX.SSE.socket(),
    ecm_figures_bbp.ecm.IVB.SSE.socket()]):
    print('---')

    results = result_values[ result_values[:,0] == arch_idx ]
#        print( results )
    nthreads = np.unique( results[:,1] )
    nthreads = np.sort(nthreads)

    mean_runtime = np.zeros_like( nthreads )
    sd_runtime   = np.zeros_like( nthreads )
    q25_perf   = np.zeros_like( nthreads )
    q75_perf   = np.zeros_like( nthreads )
    mean_mem = np.zeros_like( nthreads )
    sd_mem   = np.zeros_like( nthreads )

    #latency_per_access = np.zeros_like( nthreads )
    for i, nth in enumerate(nthreads):
        mean_runtime[i] = arch.cpu_f*np.median( 1./results[ results[:,1] == nth, -2] )
        sd_runtime[i] = arch.cpu_f*(np.quantile( 1./results[ results[:,1] == nth, -2], 0.75 ) - np.quantile( 1./results[ results[:,1] == nth, -2],0.25 ) )
        q25_perf[i] = arch.cpu_f*np.quantile( 1./results[ results[:,1] == nth, -2],0.25 )
        q75_perf[i] = arch.cpu_f*np.quantile( 1./results[ results[:,1] == nth, -2],0.75 )
        mean_mem[i] = np.mean( results[ results[:,1] == nth, -1] )
        sd_mem[i] = np.std( results[ results[:,1] == nth, -1] )

    print( arch.name, k )
    #print( latency_per_access )
    print( mean_mem[-1], '±',  sd_mem[-1] )
    print( 'single thread runtime [cy]: ', np.median(results[ results[:,1] == 1, -2]), '±', (np.quantile( results[ results[:,1] == 1, -2], 0.75 ) - np.quantile( results[ results[:,1] == 1, -2],0.25 ) ), 'performance', mean_runtime[0], '±', sd_runtime[0], q25_perf[0], q75_perf[0] )
    print( 'max thread runtime [cy]: ', np.median(results[ results[:,1] == max(nthreads), -2]), '±', (np.quantile( results[ results[:,1] == max(nthreads), -2], 0.75 ) - np.quantile( results[ results[:,1] == max(nthreads), -2],0.25 ) ), 'performance', mean_runtime[-1], '±', sd_runtime[-1], q25_perf[-1], q75_perf[-1] )

    barax.barh( [arch_idx], mean_mem[-1], xerr=sd_mem[-1], color=arch_colors[arch_idx])

    marker = 'p' if 'SKX' in arch.name else 'v'
    ax[0].errorbar( nthreads, 1e+3*mean_runtime,
            yerr = 1e+3*np.vstack(
            (np.abs( mean_runtime - q25_perf),
            np.abs( mean_runtime - q75_perf))),
        fmt=marker, color =  arch_colors[arch_idx],
        label='measured ' + arch.name, markersize=8)
    ax[0].plot( nthreads, 1e+3*mean_runtime[0]*nthreads, '-', linewidth=0.5, color=arch_colors[arch_idx] )
#        ax[0].fill_between( nthreads, 1e+3*(mean_runtime - sd_runtime), 1e+3*(mean_runtime + sd_runtime), color= arch_colors[arch_idx], alpha=0.5 )
    ax[1].plot( nthreads, mean_mem, '.-', color =  arch_colors[arch_idx])
    ax[1].fill_between( nthreads, mean_mem - sd_mem, mean_mem + sd_mem, color= arch_colors[arch_idx], alpha=0.5 )

    if 'worst-case' in args.path:
        nrn = ecm_figures_bbp.models.add_kernel( 'deliver', ecm_figures_bbp.models.L5TTPC_all_channels, ecm_figures_bbp.models.with_spike_delivery.worst_case_delivery_mixin)()
        kernel = next( _k[0] for _k in nrn.kernels if 'spike delivery' in _k[0]['name'] )
        predictions = list()
        for nth in nthreads:
            predictions.append( 1e+3*arch.cpu_f/ecm_figures_bbp.ecm.predictions.predict_runtime_from_DRAM(arch, kernel, nth) )
        print( 'predicted single thread:', ecm_figures_bbp.ecm.predictions.predict_runtime_from_DRAM(arch, kernel, 1.), 'performance', predictions[0] )
        print( 'predicted max thread:', ecm_figures_bbp.ecm.predictions.predict_runtime_from_DRAM(arch, kernel, arch.max_nthreads), 'performance', predictions[-1] )
        ax[0].plot(nthreads, predictions, '-.', color= arch_colors[arch_idx], label='all accesses latency ' + arch.name )

    elif 'best-case' in args.path:
        nrn = ecm_figures_bbp.models.add_kernel( 'deliver', ecm_figures_bbp.models.L5TTPC_all_channels, ecm_figures_bbp.models.with_spike_delivery.delivery_mixin)()
        kernel = next( _k[0] for _k in nrn.kernels if 'spike delivery' in _k[0]['name'] )
        predictions = list()
        for nth in nthreads:
            predictions.append( 1e+3*arch.cpu_f/ecm_figures_bbp.ecm.predictions.predict_runtime_from_DRAM(arch, kernel, nth) )
        ax[0].plot(nthreads, predictions, '-.', color= arch_colors[arch_idx], label='full throughput ' + arch.name )

        print( 'predicted single thread:', ecm_figures_bbp.ecm.predictions.predict_runtime_from_DRAM(arch, kernel, 1.), 'performance', predictions[0] )
        print( 'predicted max thread:', ecm_figures_bbp.ecm.predictions.predict_runtime_from_DRAM(arch, kernel, arch.max_nthreads), 'performance', predictions[-1] )

    n_accesses = kernel['accesses']
    latency_per_access = np.zeros_like( nthreads )
    for i, nth in enumerate(nthreads):
        latency_per_access[i] =  np.mean( results[ results[:,1] == nth, -2] )/(n_accesses)
#        print( 'latency per access')
#        print( latency_per_access )
    if arch_idx == 0:
        ax[1].plot( nthreads, [1740.]*nthreads.shape[0], 'k--')
        ax[0].plot( [0, 0], [0, 0], 'k--', label='model worst case memory traffic')
        ax[1].plot( nthreads, [220.]*nthreads.shape[0], '--', color='gray')
        ax[0].plot( [0, 0], [0, 0], '--', label='model best case memory traffic', color='gray')
        barax.plot( [1740., 1740.], [-0.5, 1.5], '--k')
        barax.plot( [220., 220.], [-0.5, 1.5], '--', color='gray')


ax[0].legend(bbox_to_anchor=(0., -1.35), loc='upper left', ncol=2)
ax[0].set_ylabel('Performance [Miterations/s]')
ax[1].set_ylabel('Memory data volume [B/iteration]')
ax[1].set_xlabel('Number Shared Memory Threads')
barax.set_yticks( [0,1] )
barax.set_yticklabels( ['SKX', 'IVB'])
barax.set_xlabel('Memory data volume [B/iteration]')
barax.set_axisbelow(True)

#    ax[1].set_ylim([0., 2200.])
#    ax[1].set_xlim([0., 4300])
#    ax[0].set_xscale('log', basex=10.)
#    ax[1].set_xscale('log', basex=10.)

fig.savefig('spike_delivery_multithread_'+ k + '.pdf')
barfig.savefig('spike_delivery_mem_traff_bar'+ k + '.pdf')








