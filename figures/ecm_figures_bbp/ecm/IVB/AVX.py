from . import ivb

class socket(ivb.base_ivb):
    def __init__(self):
        super().__init__()
        self.exp_thruput = 8.0 # cy per scalar iteration
        self.exp_latency = 14.4 # cy per scalar iteration
        self.name = 'IVB AVX'
