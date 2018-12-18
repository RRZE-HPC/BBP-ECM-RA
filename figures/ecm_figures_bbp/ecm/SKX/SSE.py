from . import skx

class socket(skx.base_skx):
    def __init__(self):
        super().__init__()
        self.exp_thruput = 6.7 # cy per scalar iteration
        self.exp_latency = 22.3 # cy per scalar iteration
        self.name = 'SKX SSE'
