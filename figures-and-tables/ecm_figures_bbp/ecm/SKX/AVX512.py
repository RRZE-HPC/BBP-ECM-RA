from . import skx

class socket(skx.base_skx):
    def __init__(self):
        super().__init__()
        self.exp_thruput = 1.5 # cy per scalar iteration
        self.exp_latency = 5.5 # cy per scalar iteration
        self.name = 'SKX AVX512'
