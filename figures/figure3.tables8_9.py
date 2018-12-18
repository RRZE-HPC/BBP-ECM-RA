import argparse
import numpy as np
import re
import os
import tabulate
import copy

import matplotlib
font = { 'size'   : 16 }
matplotlib.rc('font', **font)
import matplotlib.pyplot as plt

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
parser.add_argument('--latex', action='store_true',
        help='latex formatting for output table')

args = parser.parse_args()

exec( 'nrn = ' + args.model + '()' )

whole_neuron_times_singleth = list()
whole_neuron_times_maxth = list()
architectures= list()

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
    ninstances = dict()

    for irun, run in enumerate(runs):
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
                #### DEBUG
                #if 'ivb' in datadir and 'SSE' in datadir and th_idx == 1 and k[0]['name'] == 'Ih current':
                #    print( float( lines[idx + idx_meas].split(',')[5] ) )

                #pos_in_line = 5 # for average
                pos_in_line = 4 # for max
                measurements[ k_idx, th_idx, irun ] = float( lines[idx + idx_meas].split(',')[pos_in_line] )/( n_instances*tstop/nrn.dt )

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
#            if meas_name == 'linalg':
#                print('-- 1 threads -- run', run)
#                print( k[0]['name'], n_instances,
#                        lines[idx],
#                        lines[idx + idx_meas],
#                        lines[idx + idx_meas].split(',')[2], sep='\n' )

    #if 'ivb' in datadir and 'SSE' in datadir:
    #    print( runs )
    #    for k_idx, k in enumerate(nrn.kernels):
    #        print( k[0]['name'], measurements[k_idx,1,:] )

    median_meas = np.median( measurements, axis=2)
#    print(median_meas)
    iqr_meas = np.quantile( measurements, 0.75, axis=2) - np.quantile( measurements, 0.25, axis=2)
    iqr_perf = np.quantile( 1./measurements, 0.75, axis=2) - np.quantile( 1./measurements, 0.25, axis=2)
    q25_perf = np.quantile( 1./measurements, 0.25, axis=2)
    q75_perf = np.quantile( 1./measurements, 0.75, axis=2)
#    print(iqr_meas)

    predictions = np.zeros( shape=(len(nrn.kernels), len(nthreads) ) )
    for th_idx, thread in enumerate(nthreads):
        predictions[:, th_idx] = np.array(
                ecm_figures_bbp.ecm.predictions.runtime(
                    arch, nrn, nthread=thread)['DRAM'] )

    CPpredictions = np.zeros( shape=(len(nrn.kernels), len(nthreads) ) )
    for th_idx, nth in enumerate(nthreads):
        for k_idx, k in enumerate(nrn.kernels):
            if 'state' in k[0]['name']:
                new_k = copy.copy( k[0] )
                new_k['CP_bound'] = True
                CPpredictions[k_idx, th_idx] = ecm_figures_bbp.ecm.predictions.predict_runtime_from_DRAM(arch, new_k, nth)

#    predictions *= nrn.min_delay/nrn.dt
#    print( predictions )
    tabular_data = list()
    headers=['kernel',
            'single th pred [cy]',
            'single th meas [cy]',
            'error (\%)',
#            'score',
            'max th pred [cy]',
            'max th meas [cy]',
            'error (\%)']#,
#            'score' ]
    whole_neuron_row = [0.]*7
    whole_neuron_row[0] = 'whole neuron'
    for i in range(predictions.shape[0]):
        row = list()
        row.append( nrn.kernels[i][0]['name'].replace('_','\_') )
        row.append( predictions[i,0] )
        row.append( '{:.1f}'.format(median_meas[i,0]) + '$\pm$' + '{:.1f}'.format(iqr_meas[i,0]) )
        if median_meas[i,0] > 0:
            row.append( int((predictions[i,0] - median_meas[i,0])/median_meas[i,0]*100. ))
        else:
            row.append( 0 )
#        row.append( (predictions[i,0] - median_meas[i,0])/iqr_meas[i,0] )
        row.append( predictions[i,-1] )
        row.append( '{:.1f}'.format(median_meas[i,-1]) + '$\pm$' + '{:.1f}'.format(iqr_meas[i,-1])  )
        if median_meas[i,-1] > 0:
            row.append( int((predictions[i,-1] - median_meas[i,-1])/median_meas[i,-1]*100. ))
        else:
            row.append( 0 )
#        row.append( (predictions[i,-1] - median_meas[i,-1])/iqr_meas[i,-1] )

        tabular_data.append( row )

        whole_neuron_row[1] += predictions[i,0]*nrn.kernels[i][1]
        whole_neuron_row[2] += median_meas[i,0]*nrn.kernels[i][1]
        whole_neuron_row[4] += predictions[i,-1]*nrn.kernels[i][1]
        whole_neuron_row[5] += median_meas[i,-1]*nrn.kernels[i][1]

    whole_neuron_row[3] = int( (whole_neuron_row[1]-whole_neuron_row[2])/whole_neuron_row[2]*100. )
    whole_neuron_row[6] = int( (whole_neuron_row[4]-whole_neuron_row[5])/whole_neuron_row[5]*100. )

    tabular_data.append( whole_neuron_row )

    whole_neuron_times_singleth.append(  whole_neuron_row[2] )
    whole_neuron_times_maxth.append(  whole_neuron_row[5] )

    if args.latex:
        print( tabulate.tabulate( tabular_data, headers=headers,
            tablefmt='latex_raw', floatfmt = '.1f') )
    else:
        print( tabulate.tabulate( tabular_data, headers=headers) )

    to_plot = dict()
    to_plot['current'] = [
            'Im', 'exc', 'Ih']
            #'NaTs2_t', 'inh', 'Im', 'Ih']
    to_plot['state'] = [
             'exc', 'Ih', 'Im']
            #'NaTs2_t', 'Im', 'inh', 'Ih']

    for fct in ['current', 'state']:
        fig,ax = plt.subplots()
        for i in range(predictions.shape[0]):
            if nrn.kernels[i][0]['name'].split()[0] not in to_plot[fct]:
                continue
            if fct in nrn.kernels[i][0]['name']:

                scaling_factor = arch.cpu_f
                p = ax.errorbar( nthreads, scaling_factor/median_meas[i,:],
                        yerr = np.vstack(
                        (scaling_factor*np.abs( 1./median_meas[i,:] - q25_perf[i,:]),
                        scaling_factor*np.abs( 1./median_meas[i,:] - q75_perf[i,:]))),
                        label=nrn.kernels[i][0]['name'],
                        fmt='o', markersize=8 )
                if fct == 'state':
                    ax.plot( nthreads, scaling_factor/predictions[i,:], '--', linewidth=3. )
                else:
                    ax.plot( nthreads, scaling_factor/predictions[i,:], '--', linewidth=3. )
        ax.grid(which='both')
        ax.grid(which='both')
        ax.set_title(nrn.name + ' ' + arch.name + ' ' + fct)
        ax.set_ylabel('Performance [Giga/s]')
        ax.set_xlabel('Shared memory threads')
#        ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.01))
#        ax.set_yscale('log', basey=10.)
#        ax.set_xscale('log', basex=2.)
        ax.set_ylim(ymin=0.)
#        if 'ivb' in datadir and 'SSE' in datadir:
        if fct == 'current':
            ax.set_ylim(ymax = 1.3)
        else:
            ax.set_ylim(ymax = 1.3)
        fig.subplots_adjust( right=0.6, bottom=0.2 )
        fig.savefig('validate-bench_'+ arch.name.replace(' ','_') +'_' + fct + '.pdf')

