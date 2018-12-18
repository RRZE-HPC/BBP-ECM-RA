import pickle
import argparse
import numpy as np
import matplotlib
import re
import os
import tabulate

font = { 'size'   : 16 }
matplotlib.rc('font', **font)

import matplotlib.pyplot as plt
import ecm_figures_bbp

parser = argparse.ArgumentParser(description='')
parser.add_argument('--path', '-p', type=str,
        default='../results/states-and-kernels/bench_ECM_theoretical_L5_TTPC1_AVX512_tds/run0/16n/caches.txt',
        help='path to caches.txt file (including the filename)')

args = parser.parse_args()

measurements = list()
names = list()
colors = list()

single_thread = False
if '1n' in args.path:
    single_thread = True

raw_line_to_search_for = 'Raw STAT,CACHES'
if single_thread:
    raw_line_to_search_for = 'Raw'

measurements_position = 4
if single_thread:
    measurements_position = -1

with open( args.path, 'r' ) as meas_f:
    lines = meas_f.readlines()

    idx = next(i for i,v in enumerate(lines) if 'Solver Time ' in v)
    solver_time = float( lines[idx].split(':')[1] )

    line_offset = idx

    while True:
        try:
            line_offset += next(i for i,v in enumerate(lines[line_offset:]) if 'TABLE,Region' in v and raw_line_to_search_for in v)
            names.append( lines[line_offset].split(',')[1].split()[1] )
            line_offset += next(i for i,v in enumerate(lines[line_offset:]) if 'CPU_CLK_UNHALTED_CORE' in v)
            measurements.append( float( lines[line_offset].split(',')[measurements_position] ) )

#            # find a color
#            color_found = False
#            for kname, color in kernels_to_colors.items():
#                if 'exc' in kname:
#                    kname = 'DetAMPANMDA_EMS'
#                if 'inh' in kname:
#                    kname = 'DetGABAAB'
#                if 'delivery' in kname:
#                    kname = 'net_receive'
#                if 'net_receive' in names[-1]:
#                    colors.append( kernels_to_colors['delivery'] )
#                    color_found = True
#                    break
#                if kname in names[-1]:
#                    colors.append( color )
#                    color_found = True
#                    break
#            if not color_found:
#                colors.append( '#7f8b92' )

        except StopIteration:
            break

#while True:
#    try:
#        red_idx = next( i for i,v in enumerate(names) if 'reduction' in v )
#        print('Found reduction at', names[red_idx])
#    except StopIteration:
#        break
#    syn_name = '_'.join( names[red_idx].split('_')[:-2] )
#    print( syn_name + '_current' )
#    syn_pos = next( i for i,v in enumerate(names) if syn_name + '_current' in names )
#    measurements[ syn_pos ] += measurements[red_idx]
#    del names[red_idx]
#    del measurements[red_idx]
#    del colors[red_idx]

print( 'Total kernels: ', np.sum( measurements )/2.3*1e-9, 's' )
print( 'Solver Time: ', solver_time, 's' )

fig, ax = plt.subplots(figsize=(3,4.5))

bottoms = [0.,0.,0]
for m,n in zip(measurements,names):
    pos = 0 if 'current' in n else 1 if 'state' in n else 2
    tmp = [0.,0.,0]
    tmp[pos] = 100.*m/np.sum(measurements)
    plt.bar( range(3), tmp, bottom=bottoms)
    bottoms[pos] += 100.*m/np.sum(measurements)
    print( n, m )

ax.set_ylim([0.,100.])
ax.set_xticks(list(range(3)))
ax.set_xticklabels(['current', 'state', 'other'], rotation=45, ha='right')

ax.set_ylabel('Percent of total runtime')

ax.set_axisbelow(True)
ax.grid(False, axis='x')

figname = 'stacked.pdf'
fig.savefig(figname)
print( 'saved', figname )


