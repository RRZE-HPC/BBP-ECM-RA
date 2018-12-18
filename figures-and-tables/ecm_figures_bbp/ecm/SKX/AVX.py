from . import skx

class socket(skx.base_skx):
    def __init__(self):
        super().__init__()
        #self.exp_thruput = 5.9 # cy per scalar iteration
        self.exp_thruput = 3.5 # cy per scalar iteration
        self.exp_latency = 15.9 # cy per scalar iteration
        self.name = 'SKX AVX'
