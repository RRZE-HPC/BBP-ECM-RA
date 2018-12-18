from . import base
from . import kernels
from . import ion_channels

class L5TTPC(base.neuron):
    def __init__(self):
        super().__init__()
        self.n_exc_syn = 2231.
        self.n_inh_syn = 469.
        self.min_delay = 0.1
        self.dt = 0.025
        self.nseg = 913.
        self.nsec = 239.
        self.n_ion_ch_per_seg = 2.73
        self.synapse = kernels.synapse()
        self.ion_channel = kernels.ion_channel()
        self.linalg = kernels.linalg()

    @property
    def name(self):
        return super().name + 'L5TTPC'

    @property
    def n_syn(self):
        return self.n_exc_syn + self.n_inh_syn

    @property
    def n_conn(self):
        return self.n_syn
    @property
    def n_nodes(self):
        return self.nseg + self.nsec + 1.

    @property
    def kernels(self):
        # the semantics of kernels is:
        # (kernel, num instances, num repetitions in a min delay)
        return super().kernels + [
                ( self.synapse.exc_current, self.n_exc_syn, self.min_delay/self.dt ),
                ( self.synapse.inh_current, self.n_inh_syn, self.min_delay/self.dt ),
                ( self.ion_channel.current, self.n_ion_ch_per_seg*self.nseg, self.min_delay/self.dt ),
                ( self.linalg.solve, self.n_nodes, self.min_delay/self.dt ),
                ( self.synapse.exc_state, self.n_exc_syn, self.min_delay/self.dt ),
                ( self.synapse.inh_state, self.n_inh_syn, self.min_delay/self.dt ),
                ( self.ion_channel.state, self.n_ion_ch_per_seg*self.nseg, self.min_delay/self.dt )
                ]

    @property
    def memory_requirements(self):
        return super().memory_requirements + [
                ( self.synapse, self.n_exc_syn ),
                ( self.synapse, self.n_inh_syn ),
                ( self.ion_channel, self.n_ion_ch_per_seg*self.nseg ),
                ( self.linalg, self.n_nodes )
                ]

class L5TTPC_all_channels(base.neuron):
    def __init__(self):
        super().__init__()
        self.n_exc_syn = 2231.
        self.n_inh_syn = 469.
        self.min_delay = 0.1
        self.dt = 0.025
        self.nseg = 913.
        self.nsec = 239.
        self.synapse = kernels.synapse()
        self.linalg = kernels.linalg()

    @property
    def name(self):
        return super().name + 'L5TTPC'

    @property
    def n_syn(self):
        return self.n_exc_syn + self.n_inh_syn

    @property
    def n_conn(self):
        return self.n_syn
    @property
    def n_nodes(self):
        return self.nseg + self.nsec + 1.

    @property
    def kernels(self):
        # the semantics of kernels is:
        # (kernel, num instances, num repetitions in a min delay)
        return super().kernels + [
                ( self.synapse.exc_current, self.n_exc_syn, self.min_delay/self.dt ),
                ( self.synapse.inh_current, self.n_inh_syn, self.min_delay/self.dt ),
                ( ion_channels.NaTs2_t().current, 520., self.min_delay/self.dt ),
                ( ion_channels.Ih().current, 911., self.min_delay/self.dt ),
                ( ion_channels.Im().current, 519., self.min_delay/self.dt ),
                ( ion_channels.SKv3_1().current, 522., self.min_delay/self.dt ),
                ( self.linalg.solve, self.n_nodes, self.min_delay/self.dt ),
                ( self.synapse.exc_state, self.n_exc_syn, self.min_delay/self.dt ),
                ( self.synapse.inh_state, self.n_inh_syn, self.min_delay/self.dt ),
                ( ion_channels.NaTs2_t().state, 520., self.min_delay/self.dt ),
                ( ion_channels.Ih().state, 911., self.min_delay/self.dt ),
                ( ion_channels.Im().state, 519., self.min_delay/self.dt ),
                ( ion_channels.SKv3_1().state, 522., self.min_delay/self.dt )
                ]

    @property
    def memory_requirements(self):
        return super().memory_requirements + [
                ( self.synapse, self.n_exc_syn ),
                ( self.synapse, self.n_inh_syn ),
                ( ion_channels.NaTs2_t, 520. ),
                ( ion_channels.Ih, 911. ),
                ( ion_channels.Im,  519. ),
                ( ion_channels.SKv3_1, 522. ),
                ( self.linalg, self.n_nodes )
                ]


