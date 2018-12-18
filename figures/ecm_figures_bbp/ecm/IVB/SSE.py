from . import ivb

class socket(ivb.base_ivb):
    def __init__(self):
        super().__init__()
        self.exp_thruput = 11.5 # cy per scalar iteration
        self.exp_latency = 29.5 # cy per scalar iteration
        self.name = 'IVB SSE'
