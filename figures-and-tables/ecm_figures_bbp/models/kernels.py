# All quantities (throughput, time, reads, etc..) are *per scalar iteration*.

class synapse():
    n_state_vars =  16
    n_params =  14
    avg_len_seq_of_same_nd_indices = 3.
    def __init__(self):
        self.name = 'synapses'
        self.exc_current = dict(
                name = 'exc syn current',
                reads  = 6 + 2*0.5 + 2./self.avg_len_seq_of_same_nd_indices,
                writes = 9,
                iaca_Thruput = {
                    "IVB.SSE": 21,
                    "IVB.AVX": 21,
                    "SKX.SSE": 14.9,
                    "SKX.AVX": 10,
                    "SKX.AVX512": 5.7},
                iaca_Tload = {
                    "IVB.SSE": 9.75,
                    "IVB.AVX": 7.75,
                    "SKX.SSE": 9.9,
                    "SKX.AVX": 7,
                    "SKX.AVX512": 3.5},
                nexp = 1
                )
        self.exc_state = dict(
                name = 'exc syn state',
                reads  = 4,
                writes = 4,
                iaca_Thruput = {
                    "IVB.SSE": 29,
                    "IVB.AVX": 28,
                    "SKX.SSE": 8,
                    "SKX.AVX": 8,
                    "SKX.AVX512": 3.7},
                iaca_Tload = {
                    "IVB.SSE": 5,
                    "IVB.AVX": 3.9,
                    "SKX.SSE": 6.5,
                    "SKX.AVX": 3.75,
                    "SKX.AVX512": 1.7},
                iaca_CP = {
                    "IVB.SSE": 91./2.,
                    "IVB.AVX": 163./4.,
                    "SKX.SSE": 91./2.,
                    "SKX.AVX": 162./4.,
                    "SKX.AVX512": 162./4.},
                nexp = 4
                )
        self.inh_current = dict(
                name = 'inh syn current',
                reads  = 5 + 2*0.5 + 2./self.avg_len_seq_of_same_nd_indices,
                writes = 8,
                iaca_Thruput = {
                    "IVB.SSE": 18.05/2.,
                    "IVB.AVX": 29.55/4.,
                    "SKX.SSE": 18./2.,
                    "SKX.AVX": 29.47/4.,
                    "SKX.AVX512": 28.89/8.},
                iaca_Tload = {
                    "IVB.SSE": 14./2.,
                    "IVB.AVX": 24./4.,
                    "SKX.SSE": 15./2.,
                    "SKX.AVX": 22.6/4.,
                    "SKX.AVX512": 20./8.},
                nexp = 0
                )
        self.inh_state = dict(
                name = 'inh syn state',
                reads  = 4,
                writes = 4,
                iaca_Thruput = {
                    "IVB.SSE": 29,
                    "IVB.AVX": 28,
                    "SKX.SSE": 8,
                    "SKX.AVX": 8,
                    "SKX.AVX512": 3.7},
                iaca_Tload = {
                    "IVB.SSE": 5,
                    "IVB.AVX": 3.9,
                    "SKX.SSE": 6.5,
                    "SKX.AVX": 3.75,
                    "SKX.AVX512": 1.7},
                iaca_CP = {
                    "IVB.SSE": 91./2.,
                    "IVB.AVX": 163./4.,
                    "SKX.SSE": 91./2.,
                    "SKX.AVX": 162./4.,
                    "SKX.AVX512": 162./4.},
                nexp = 4
                )

class filt_synapse():
    n_state_vars =  18
    n_params =  15
    def __init__(self):
        self.name = 'filtered synapses'
        self.exc_current = dict(
                name = 'exc filtered synapse current',
                reads  = 9.1,
                writes = 10,
                iaca_Thruput = {
                    #"IVB.SSE": 21.,
                    "IVB.SSE": 68./2., #latency
                    "IVB.AVX": 21.,
                    "SKX.SSE": 15.5,
                    "SKX.AVX": 44.74/4.,
                    "SKX.AVX512": 47.53/8.},
                iaca_Tload = {
                    "IVB.SSE": 10.5,
                    "IVB.AVX": 8.25,
                    "SKX.SSE": 10.8,
                    "SKX.AVX": 31./4.,
                    "SKX.AVX512": 28./8.},
                nexp = 1
                )
        self.exc_state = dict(
                name = 'exc filtered synapse state',
                reads  = 6,
                writes = 5,
                iaca_Thruput = {
                    "IVB.SSE": 50.4,
                    "IVB.AVX": 49,
                    "SKX.SSE": 13.8,
                    "SKX.AVX": 55.79/4.,
                    "SKX.AVX512": 46.47/8.},
                iaca_Tload = {
                    "IVB.SSE": 7.,
                    "IVB.AVX": 5.75,
                    "SKX.SSE": 8.5,
                    "SKX.AVX": 20.5/4.,
                    "SKX.AVX512": 21./8.},
                nexp = 5
                )
        self.inh_current = dict(
                name = 'inh filtered synapse current',
                reads  = 8.1,
                writes = 9,
                iaca_Thruput = {
                    "IVB.SSE": 19.65/2.,
                    "IVB.AVX": 31.6/4.,
                    "SKX.SSE": 19.47/2.,
                    "SKX.AVX": 31.95/4.,
                    "SKX.AVX512": 32.16/8.},
                iaca_Tload = {
                    "IVB.SSE": 15./2.,
                    "IVB.AVX": 27./4.,
                    "SKX.SSE": 15.1/2.,
                    "SKX.AVX": 24./4.,
                    "SKX.AVX512": 23./8.},
                nexp = 0
                )
        self.inh_state = dict(
                name = 'inh filtered synapse state',
                reads  = 6,
                writes = 5,
                iaca_Thruput = {
                    "IVB.SSE": 98./2.,
                    "IVB.AVX": 196./4.,
                    "SKX.SSE": 27.79/2.,
                    "SKX.AVX": 55.79/4.,
                    "SKX.AVX512": 45.63/8.},
                iaca_Tload = {
                    "IVB.SSE": 7.,
                    "IVB.AVX": 23./4.,
                    "SKX.SSE": 17./2.,
                    "SKX.AVX": 20.5/4.,
                    "SKX.AVX512": 18./8.},
                nexp = 5
                )

class ion_channel():
    n_state_vars =  8.5
    n_params =  1
    # an average only for L5_TTPC cell
    def __init__(self):
        self.name = 'ion channels'
        self.current = dict(
                name = 'ion channel current',
                reads  = 4.97,
                writes = 5.26,
                iaca_Thruput = {
                    "IVB.SSE": 6.78,
                    "IVB.AVX": 6.70,
                    "SKX.SSE": 6.92,
                    "SKX.AVX": 7.64,
                    "SKX.AVX512": 4.68},
                iaca_Tload = {
                    "IVB.SSE": 4.50,
                    "IVB.AVX": 4.53,
                    "SKX.SSE": 4.50,
                    "SKX.AVX": 4.79,
                    "SKX.AVX512": 2.56},
                nexp = 0
                )
        self.state = dict(
                name = 'ion channel state',
                reads  = 1.5,
                writes = 5.63,
                iaca_Thruput = {
                    "IVB.SSE": 69.25,
                    "IVB.AVX": 69.25,
                    "SKX.SSE": 19.68,
                    "SKX.AVX": 19.73,
                    "SKX.AVX512": 9.74},
                iaca_Tload = {
                    "IVB.SSE": 5.55,
                    "IVB.AVX": 4.84,
                    "SKX.SSE": 6.90,
                    "SKX.AVX": 4.62,
                    "SKX.AVX512": 2.16},
                nexp = 3.63
                #5.14 # taken from old detailed_neuron/kernels/ion_channel_state.py
                )

class gif():
    n_state_vars =  12
    n_params =  11
    def __init__(self):
        self.name = 'gif'
        self.current = dict(
                name = 'gif current',
                reads  = 14.,
                writes = 8.,
                iaca_Thruput = {
                    "IVB.SSE": 28./2.,
                    "IVB.AVX": 56./4.,
                    "SKX.SSE": 26.95/2.,
                    "SKX.AVX": 38./4.,
                    "SKX.AVX512": 55./8.},
                iaca_Tload = {
                    "IVB.SSE": 20.5/2.,
                    "IVB.AVX": 30.5/4.,
                    "SKX.SSE": 21.6/2.,
                    "SKX.AVX": 29.5/4.,
                    "SKX.AVX512": 27./8.},
                nexp = 2
                )
        self.state = dict(
                name = 'gif state',
                reads  = 7,
                writes = 6,
                iaca_Thruput = {
                    "IVB.SSE": 128./2.,
                    "IVB.AVX": 253./4.,
                    "SKX.SSE": 18.,
                    "SKX.AVX": 18.,
                    "SKX.AVX512": 156/8.},
                iaca_Tload = {
                    "IVB.SSE": 14.5/2.,
                    "IVB.AVX": 22./4.,
                    "SKX.SSE": 17.5/2.,
                    "SKX.AVX": 5.5,
                    "SKX.AVX512": 50/8.},
                nexp = 6
                )

class iaf():
    n_state_vars = 9
    n_params = 19
    def __init__(self):
        self.name = 'iaf'
        self.update = dict(
                name = 'iaf update',
                reads  = 11,
                writes = 5,
                iaca_Thruput = {
                    "IVB.SSE": 15.5/2.,
                    "IVB.AVX": 26.55/4.,
                    "SKX.SSE": 15.37/2.,
                    "SKX.AVX": 26.53/4.,
                    "SKX.AVX512": 19.26/8.},
                iaca_Tload = {
                    "IVB.SSE": 13/2.,
                    "IVB.AVX": 25.5/4.,
                    "SKX.SSE": 13/2.,
                    "SKX.AVX": 22.6/4.,
                    "SKX.AVX512": 14./8.},
                nexp = 0
                )
        self.psc = dict(
                name= 'iaf psc',
                reads  = 2,
                writes = 4,
                iaca_Thruput = {
                    "IVB.SSE": 5./2.,
                    "IVB.AVX": 8.3/4.,
                    "SKX.SSE": 5./2.,
                    "SKX.AVX": 5./4.,
                    "SKX.AVX512": 5./8.},
                iaca_Tload = {
                    "IVB.SSE": 3./2.,
                    "IVB.AVX": 6/4.,
                    "SKX.SSE": 3./2.,
                    "SKX.AVX": 3./4.,
                    "SKX.AVX512": 3./8.},
                nexp = 0
                )

class linalg():
    n_state_vars =  3.5 + 1 #matrix elements, parent index, node area
    n_params =  0
    def __init__(self):
        self.name = 'linear algebra'
        self.solve = dict(
                name = 'linear algebra',
                reads  = 4 + 2*0.5,
                writes = 3.,
                iaca_Thruput = {
                    "IVB.SSE": 14. + 14.,
                    "IVB.AVX": 14. + 14.,
                    "SKX.SSE": 4.52 + 3.6,
                    "SKX.AVX": 4.52 + 3.6,
                    "SKX.AVX512": 4.52 + 3.6},
                iaca_Tload = {
                    "IVB.SSE": 3.5 + 2.5,
                    "IVB.AVX": 3.5 + 2.5 ,
                    "SKX.SSE": 3.5 + 2.5,
                    "SKX.AVX": 3.5 + 2.5,
                    "SKX.AVX512": 3.5 + 2.5},
                iaca_CP = {
                    "IVB.SSE": 20. + 20.,
                    "IVB.AVX": 20. + 20.,
                    "SKX.SSE": 14. + 14.,
                    "SKX.AVX": 14. + 14.,
                    "SKX.AVX512": 14. + 14.},
                vectorizable=False,
                nexp = 0
                )

class spike_delivery():
    n_state_vars =  0
    n_params =  0
    def __init__(self):
        self.name = 'spike delivery'
        n_dbl_overhead = 0.#1
        n_int_overhead = 3.#8
        n_pnt_overhead = 1.#5
        self.AMPA = dict(
                name = 'AMPA spike delivery',
                reads  = 7 + (n_dbl_overhead + n_pnt_overhead + n_int_overhead*0.5), # adding overhead from calls to net_buf_receive
                writes = 8 + 1, # + 1 for tsav = t,
                accesses = 7.+ 9.*2. + 2.,
                iaca_Thruput = {
                    "IVB.SSE": 29.5,
                    "IVB.AVX": 29.5,
                    "SKX.SSE": 27.58,
                    "SKX.AVX": 27.58,
                    "SKX.AVX512": 27.58},
                iaca_CP = {
                    "IVB.SSE": 79.,
                    "IVB.AVX": 79.,
                    "SKX.SSE": 79.,
                    "SKX.AVX": 79.,
                    "SKX.AVX512": 79.},
                iaca_Tload = {
                    "IVB.SSE": 19.5,
                    "IVB.AVX": 19.5,
                    "SKX.SSE": 19.5,
                    "SKX.AVX": 19.5,
                    "SKX.AVX512": 19.5},
                vectorizable=False,
                CP_bound = True,
                nexp = 2
                )
        self.CUBA = dict(
                # comput theoretically, loop is
                # psc = psc + w*constant
                name = 'CUBA spike delivery',
                reads  = 1 + (n_dbl_overhead + n_pnt_overhead + n_int_overhead*0.5), # adding overhead from calls to net_buf_receive
                writes = 1 + 1,
                iaca_Thruput = {
                    "IVB.SSE": 1./2.,
                    "IVB.AVX": 2./4.,
                    "SKX.SSE": 1./2.,
                    "SKX.AVX": 1./4.,
                    "SKX.AVX512": 1./8.},
                iaca_Tload = {
                    "IVB.SSE": 1./2.,
                    "IVB.AVX": 2./4.,
                    "SKX.SSE": 1./2.,
                    "SKX.AVX": 1./4.,
                    "SKX.AVX512": 1./8.},
                vectorizable=False,
                nexp = 0
                )



class spike_delivery_worstCaseMemAccess():
    n_state_vars =  0
    n_params =  0
    def __init__(self):
        self.name = 'spike delivery'
        n_dbl_overhead = 0.#1
        n_int_overhead = 3.#8
        n_pnt_overhead = 1.#5
        self.AMPA = dict(
                name = 'AMPA spike delivery - worst case',
                reads  = (7 + (n_dbl_overhead + n_pnt_overhead + n_int_overhead*0.5) )*8,  # adding overhead from calls to net_buf_receive
                writes = (8+1)*8,
                accesses = 7.+9.*2.+2.,
                iaca_Thruput = {
                    "IVB.SSE": 29.5,
                    "IVB.AVX": 29.5,
                    "SKX.SSE": 27.58,
                    "SKX.AVX": 27.58,
                    "SKX.AVX512": 27.58},
                iaca_CP = {
                    "IVB.SSE": 79.,
                    "IVB.AVX": 79.,
                    "SKX.SSE": 79.,
                    "SKX.AVX": 79.,
                    "SKX.AVX512": 79.},
                iaca_Tload = {
                    "IVB.SSE": 19.5,
                    "IVB.AVX": 19.5,
                    "SKX.SSE": 19.5,
                    "SKX.AVX": 19.5,
                    "SKX.AVX512": 19.5},
                vectorizable=False,
                latency_bound=True,
                CP_bound = True,
                nexp = 2
                )
        self.CUBA = dict(
                # comput theoretically, loop is
                # psc = psc + w*constant
                name = 'CUBA spike delivery - worst case',
                reads  = (1 + (n_dbl_overhead + n_pnt_overhead + n_int_overhead*0.5))*8,  # adding overhead from calls to net_buf_receive
                writes = (1+1)*8,
                iaca_Thruput = {
                    "IVB.SSE": 1./2.,
                    "IVB.AVX": 2./4.,
                    "SKX.SSE": 1./2.,
                    "SKX.AVX": 1./4.,
                    "SKX.AVX512": 1./8.},
                iaca_Tload = {
                    "IVB.SSE": 1./2.,
                    "IVB.AVX": 2./4.,
                    "SKX.SSE": 1./2.,
                    "SKX.AVX": 1./4.,
                    "SKX.AVX512": 1./8.},
                vectorizable=False,
                nexp = 0
                )

class stdp():
    n_state_vars =  4
    n_params =  9
    def __init__(self):
        self.name = 'stdp'
        # corresponds to STDPConnection< targetidentifierT >::send
        # gets called when a neuron under consideration is the target of an stdp connection
        # consider on average that only one post-synaptic spike gets retrieved
        self.postsyn = dict(
                name = 'postsyn stdp',
                # read: tau_plus_, lambda_, alpha_, mu_plus_
                #        mu_minus_, Wmax_, target_tau_minus_inv_, dendritic_delay
                #        target_last_spike
                # write: weights, target_Kminus_, Kplus_, t_lastspike_
                reads  = 9,
                writes = 4,
                iaca_Thruput = {
                    "IVB.SSE": 56.,
                    "IVB.AVX": 56.,
                    "SKX.SSE": 25.26,
                    "SKX.AVX": 25.26,
                    "SKX.AVX512": 25.26},
                iaca_Tload = {
                    "IVB.SSE": 20.,
                    "IVB.AVX": 20.,
                    "SKX.SSE": 20.,
                    "SKX.AVX": 20.,
                    "SKX.AVX512": 20.},
                vectorizable=False,
                nexp = 3 + 2 # simplification pow = exp
                )

class stdp_worstCaseMemAccess():
    n_state_vars =  4
    n_params =  9
    def __init__(self):
        self.name = 'stdp'
        # corresponds to STDPConnection< targetidentifierT >::send
        # gets called when a neuron under consideration is the target of an stdp connection
        # consider on average that only one post-synaptic spike gets retrieved
        self.postsyn = dict(
                name = 'postsyn stdp - worst case',
                # read: tau_plus_, lambda_, alpha_, mu_plus_
                #        mu_minus_, Wmax_, target_tau_minus_inv_, dendritic_delay
                #        target_last_spike
                # write: weights, target_Kminus_, Kplus_, t_lastspike_
                reads  = 9*8,
                writes = 4*8,
                iaca_Thruput = {
                    "IVB.SSE": 56.,
                    "IVB.AVX": 56.,
                    "SKX.SSE": 25.26,
                    "SKX.AVX": 25.26,
                    "SKX.AVX512": 25.26},
                iaca_Tload = {
                    "IVB.SSE": 20.,
                    "IVB.AVX": 20.,
                    "SKX.SSE": 20.,
                    "SKX.AVX": 20.,
                    "SKX.AVX512": 20.},
                vectorizable=False,
                nexp = 3 + 2 # simplification pow = exp
                )


class queue_ops():
    n_state_vars =  0
    n_params =  0
    def __init__(self):
        self.name = 'queue operations'
        self.binq = dict(
                name = 'binq operations',
                reads = 0.,
                writes = 0.,
                iaca_Thruput = {
                    "IVB.SSE": 0.,
                    "IVB.AVX": 0.,
                    "SKX.SSE": 0.,
                    "SKX.AVX": 0.,
                    "SKX.AVX512": 0.},
                iaca_Tload = {
                    "IVB.SSE": 0.,
                    "IVB.AVX": 0.,
                    "SKX.SSE": 0.,
                    "SKX.AVX": 0.,
                    "SKX.AVX512": 0.},
                vectorizable=False,
                nexp = 0
                )

