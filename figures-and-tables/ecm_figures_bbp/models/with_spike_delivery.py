from . import kernels
from . import base

def add_kernel(name, base, extension):
    return type(name, (base, extension), dict() )

class delivery_mixin(base.neuron):
    def __init__(self):
        super().__init__()
        self.AMPAspk = kernels.spike_delivery().AMPA
        self.firing_freq = 1. # Hz

    @property
    def name(self):
        return super().name + ' +delivery '

    @property
    def kernels(self):
        return super().kernels + [(self.AMPAspk,
                    self.n_conn*self.dt*self.firing_freq*1e-3,
                    self.min_delay/self.dt ) ]

class CUBA_delivery_mixin(base.neuron):
    def __init__(self):
        super().__init__()
        self.CUBAspk = kernels.spike_delivery().CUBA
        self.firing_freq = 1. # Hz

    @property
    def name(self):
        return super().name + ' +delivery '

    @property
    def kernels(self):
        return super().kernels + [(self.CUBAspk,
                    self.n_conn*self.dt*self.firing_freq*1e-3,
                    self.min_delay/self.dt ) ]

class worst_case_delivery_mixin(base.neuron):
    def __init__(self):
        super().__init__()
        self.wAMPAspk = kernels.spike_delivery_worstCaseMemAccess().AMPA
        self.firing_freq = 1. # Hz

    @property
    def name(self):
        return super().name + ' +worst_case_delivery '

    @property
    def kernels(self):
        return super().kernels + [(self.wAMPAspk,
                    self.n_conn*self.dt*self.firing_freq*1e-3,
                    self.min_delay/self.dt ) ]

class worst_case_CUBA_delivery_mixin(base.neuron):
    def __init__(self):
        super().__init__()
        self.wCUBAspk = kernels.spike_delivery_worstCaseMemAccess().CUBA
        self.firing_freq = 1. # Hz

    @property
    def name(self):
        return super().name + ' +worst_case_delivery '

    @property
    def kernels(self):
        return super().kernels + [(self.wCUBAspk,
                    self.n_conn*self.dt*self.firing_freq*1e-3,
                    self.min_delay/self.dt ) ]


class stdp_mixin(base.neuron):
    def __init__(self):
        super().__init__()
        self.plast = kernels.stdp().postsyn
        self.ratio_plastic_conn = 0.8*0.8 #80% of plastic synapses

    @property
    def name(self):
        return super().name + ' +stdp '

    @property
    def kernels(self):
        return super().kernels + [( self.plast,
                    self.n_conn*self.ratio_plastic_conn*self.dt*self.firing_freq*1e-3,
                    self.min_delay/self.dt ) ]

class worst_case_stdp_mixin(base.neuron):
    def __init__(self):
        super().__init__()
        self.wplast = kernels.stdp_worstCaseMemAccess().postsyn
        self.ratio_plastic_conn = 0.8*0.8 #80% of plastic synapses

    @property
    def name(self):
        return super().name + ' +worst_case_stdp '

    @property
    def kernels(self):
        return super().kernels + [( self.wplast,
                    self.n_conn*self.ratio_plastic_conn*self.dt*self.firing_freq*1e-3,
                    self.min_delay/self.dt ) ]

class queue_ops_mixin(base.neuron):
    def __init__(self):
        super().__init__()
        self.queue = kernels.queue_ops().binq

    @property
    def name(self):
        return super().name + ' +binq '

    @property
    def kernels(self):
        return super().kernels + [(self.queue,
                    self.n_conn*self.dt*self.firing_freq*1e-3,
                    self.min_delay/self.dt ) ]

