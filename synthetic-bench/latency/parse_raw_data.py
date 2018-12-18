from __future__ import print_function
import re
import numpy as np
#import tabulate

with open("raw_data.dat", "r") as f:
    lines = f.readlines()

nlines = len(lines)

table = list()

for i in range(nlines):
    line = lines[i]
    if 'No such file or directory' in line:
        continue
    if 'Memory data volume' in line:
        sz = float( line.split('|')[0].split('.')[-4].split('z')[-1] )
        nrep = float( line.split('|')[0].split('.')[-3].split('p')[-1] )
        data_vol = float( line.split('|')[-2] )
    if 'CPU_CLK_UNHALTED_CORE' in line:
        clock = float( line.split('|')[-2] )

        expected_B_per_iter = 0.
        avg_latency_per_access = 0.
        tot_prob_sz = 0.
        if 'streams' in line:
            n_streams = float( re.search( '[0-9]+', line.split('/')[0]).group() )
            expected_B_per_iter += n_streams*1.5*64.
            tot_prob_sz = 8.*sz*n_streams*1e-6
            if 'traversal' in line:
                expected_B_per_iter += 64.
                avg_latency_per_access += clock/(nrep*sz*(1 + n_streams*1.5))
                tot_prob_sz += 4*sz*1e-6
            else:
                expected_B_per_iter += 4.
                avg_latency_per_access += clock/(nrep*sz*n_streams*1.5)
        elif 'traversal' in line:
            if 'double' in line:
                expected_B_per_iter += 128.
                n_streams = -2
                avg_latency_per_access += clock/(nrep*sz*2.)
                tot_prob_sz = 2.*4*sz*1e-6
            else:
                expected_B_per_iter += 64.
                n_streams = -1
                avg_latency_per_access += clock/(nrep*sz)
                tot_prob_sz = 4*sz*1e-6

        print( nrep, sz, data_vol, data_vol*1e+9/(nrep*sz),
                expected_B_per_iter, clock, clock/(nrep*sz),
                n_streams, avg_latency_per_access,
                tot_prob_sz )

        table.append( [nrep, sz, data_vol, data_vol*1e+9/(nrep*sz),
            expected_B_per_iter, clock, clock/(nrep*sz),
            n_streams, avg_latency_per_access,
            tot_prob_sz ] )

headers = [
        'nrep', 'size', 'data vol',
        'B/iter', 'Expect B/iter',
        'CPU CLOCK', 'cy/iter',
        'n stream', 'avg lat/access',
        'prob size' ]

#print( tabulate.tabulate( table, headers=headers ) )
table = np.array( table )
#print(table)

