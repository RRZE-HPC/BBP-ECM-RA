import pandas as pd
from collections import OrderedDict
from copy import copy

def predict_runtime_from_DRAM( arch, kernel, nthread=1.):
    TMem = arch.TMem( kernel )
    latency_bound = kernel['latency_bound'] if 'latency_bound' in kernel else False
    if latency_bound:
        kernel_copy = copy( kernel )
        del kernel_copy['latency_bound']
        T_BW = arch.TMem( kernel_copy )
        TMem = max( T_BW, TMem/nthread)
    single_thread_prediction = arch.predictions( kernel )['DRAM']
    parallel_portion = single_thread_prediction - TMem
    return TMem + max( parallel_portion/nthread - (nthread-1)/nthread*TMem, 0. )


def runtime(arch, nrn, nthread=1.):
    predictions = OrderedDict()
    columns = ['L1', 'L2', 'L3']
    for k in nrn.kernels:
        predictions[ k[0]['name'] ] = list()
        for c in columns:
            predictions[ k[0]['name'] ].append( arch.predictions( k[0] )[c]/nthread )
        predictions[ k[0]['name'] ].append(
                predict_runtime_from_DRAM(
                    arch, k[0], nthread ) )

    columns.append( 'DRAM' )

    return pd.DataFrame.from_dict(predictions, orient='index', columns=columns)

def saturation(arch, nrn):
    predictions = OrderedDict()
    for k in nrn.kernels:
        predictions[ k[0]['name'] ] = [ arch.TMem( k[0] ) ]
        predictions[ k[0]['name'] ].append(
                arch.predictions( k[0] )['DRAM']/arch.TMem( k[0] ) )

    return pd.DataFrame.from_dict(predictions, orient='index', columns=['runtime', 'n'])

def ecm_model(arch, nrn):
    ecm_model = OrderedDict()
    column_name = ['TOL', 'TnOL', 'L1L2', 'L2L3', 'L3DRAM']
    columns = [arch.TOL, arch.TnOL, arch.TL1L2, arch.TL2L3, arch.TMem]
    for k in nrn.kernels:
        ecm_model[ k[0]['name'] ] = list()
        for c in columns:
            ecm_model[ k[0]['name'] ].append( c(k[0]) )

    return pd.DataFrame.from_dict(ecm_model, orient='index', columns=column_name)

def contributions(arch, nrn, nthread=1.):
    contributions = OrderedDict()
    for k in nrn.kernels:
        contributions[ k[0]['name'] ] = arch.rate_limiting_steps( k[0] )
        if nthread > 1.:
            # compute adjustment for multi-threading
            for data_orig in ['L1', 'L2', 'L3']:
                for key, val in contributions[ k[0]['name'] ][data_orig].items():
                    contributions[ k[0]['name'] ][data_orig][key] /= nthread
            # special treatment for DRAM
            TMem = arch.TMem( k[0] )
            single_thread_prediction = arch.predictions( k[0] )['DRAM']
            parallel_portion = single_thread_prediction - TMem
            if 'Tload' in contributions[ k[0]['name'] ]['DRAM']:
                if parallel_portion/nthread - (nthread-1)/nthread*TMem > 0.:
                    contributions[ k[0]['name'] ]['DRAM']['Tload'] /= nthread
                    contributions[ k[0]['name'] ]['DRAM']['Tload'] -= (nthread-1.)/nthread*TMem
                    contributions[ k[0]['name'] ]['DRAM']['TL1L2'] /= nthread
                    contributions[ k[0]['name'] ]['DRAM']['TL1L2'] -= (nthread-1.)/nthread*TMem
                    contributions[ k[0]['name'] ]['DRAM']['TL2L3'] /= nthread
                    contributions[ k[0]['name'] ]['DRAM']['TL2L3'] -= (nthread-1.)/nthread*TMem
                else:
                    contributions[ k[0]['name'] ]['DRAM']['Tload'] = 0.
                    contributions[ k[0]['name'] ]['DRAM']['TL1L2'] = 0.
                    contributions[ k[0]['name'] ]['DRAM']['TL2L3'] = 0.
            else:
                for key, val in contributions[ k[0]['name'] ]['DRAM'].items():
                    contributions[ k[0]['name'] ]['DRAM'][key] /= nthread

    return pd.DataFrame.from_dict(contributions, orient='index').reset_index().set_index('index').rename_axis('kernel')

def mem_traffic( kernel ):
    return 8.*( kernel['reads'] + 2.*kernel['writes'])



