from collections import defaultdict
from collections import OrderedDict

class base_ivb():
    def __init__(self):
        self.cache_BW = 32. # B/cy
        self.mem_BW   = 40. # GB/s
        self.cpu_f    = 2.2 # GHz
        self.L1_latency = 4. # cy per access, from https://www.7-cpu.com/cpu/Skylake.html
        self.L2_latency = 12. # cy per access, from https://www.7-cpu.com/cpu/Skylake.html
        self.L3_latency = 12. # cy per access, dummy number for now
        #self.mem_latency = 18.5  # cy per access, benchmarks
        self.mem_latency = 20.  # cy per access, benchmarks
        #self.mem_latency = 37.5 # cy per access, cheat from bench
        self.max_nthreads = 10.
        self.scalar_exp_thruput = 27.8 #cy
        self.scalar_exp_latency = 64. #cy -- should substract latency of minus op?


    def TOL(self, kernel):
        vectorizable = kernel['vectorizable'] if 'vectorizable' in kernel else True
        CP_bound = kernel['CP_bound'] if 'CP_bound' in kernel else False

        if not CP_bound:
            if vectorizable:
                return kernel['iaca_Thruput'][self.name.replace(' ','.')] + kernel['nexp']*self.exp_thruput
            else:
                return kernel['iaca_Thruput'][self.name.replace(' ','.')] + kernel['nexp']*self.scalar_exp_thruput
        else:
            if vectorizable:
                return kernel['iaca_CP'][self.name.replace(' ','.')] + kernel['nexp']*self.exp_latency
            else:
                return kernel['iaca_CP'][self.name.replace(' ','.')] + kernel['nexp']*self.scalar_exp_latency

    def TnOL(self, kernel):
        latency_bound = kernel['latency_bound'] if 'latency_bound' in kernel else False
        if not latency_bound:
            return kernel['iaca_Tload'][self.name.replace(' ','.')]
        else:
            return (kernel['accesses'])*self.L1_latency

    def TL1L2(self, kernel):
        latency_bound = kernel['latency_bound'] if 'latency_bound' in kernel else False
        if not latency_bound:
            return 8.*(kernel['reads'] + 2.*kernel['writes'])/self.cache_BW
        else:
            return (kernel['accesses'])*self.L2_latency

    def TL2L3(self, kernel):
        latency_bound = kernel['latency_bound'] if 'latency_bound' in kernel else False
        if not latency_bound:
            return 8.*(kernel['reads'] + 2.*kernel['writes'])/self.cache_BW
        else:
            return (kernel['reads'])*self.L3_latency

    def TMem(self, kernel):
        latency_bound = kernel['latency_bound'] if 'latency_bound' in kernel else False
        if not latency_bound:
            return 8.*(kernel['reads'] + 2.*kernel['writes'])/self.mem_BW*self.cpu_f
        else:
            return (kernel['accesses'])*self.mem_latency

    def predictions(self, kernel):
        latency_bound = kernel['latency_bound'] if 'latency_bound' in kernel else False
        return dict(
                L1   = max( self.TOL(kernel), self.TnOL(kernel)),
                L2   = max( self.TOL(kernel), self.TnOL(kernel) + self.TL1L2(kernel)),
                L3   = max( self.TOL(kernel), self.TnOL(kernel) + self.TL1L2(kernel) + self.TL2L3(kernel)),
                DRAM = max( self.TOL(kernel), self.TnOL(kernel) + self.TL1L2(kernel) + self.TL2L3(kernel) + self.TMem(kernel)) if not latency_bound else max( self.TOL(kernel), self.TMem(kernel) )
                )

    def core_rate_limiting_steps(self,kernel):
        try:
            vectorizable = kernel['vectorizable']
        except KeyError:
            vectorizable = True
        if vectorizable:
            return (kernel['iaca_Thruput'][self.name.replace(' ','.')], kernel['nexp']*self.exp_thruput)
        else:
            return (kernel['iaca_Thruput'][self.name.replace(' ','.')], kernel['nexp']*self.scalar_exp_thruput)

    def rate_limiting_steps(self, kernel):
        contributions = OrderedDict()
        contributions['L1'] = defaultdict(float)
        if self.TOL(kernel) > self.TnOL(kernel):
            contributions['L1']['core'], contributions['L1']['exp'] = self.core_rate_limiting_steps( kernel )
        else:
            contributions['L1']['Tload'] = self.TnOL( kernel )

        contributions['L2'] = defaultdict(float)
        if self.TOL(kernel) > self.TnOL(kernel) + self.TL1L2(kernel):
            contributions['L2']['core'], contributions['L2']['exp'] = self.core_rate_limiting_steps( kernel )
        else:
            contributions['L2']['Tload'] = self.TnOL( kernel )
            contributions['L2']['TL1L2'] = self.TL1L2( kernel )

        contributions['L3'] = defaultdict(float)
        if self.TOL(kernel) > self.TnOL(kernel) + self.TL1L2(kernel) + self.TL2L3(kernel):
            contributions['L3']['core'], contributions['L3']['exp'] = self.core_rate_limiting_steps( kernel )
        else:
            contributions['L3']['Tload'] = self.TnOL( kernel )
            contributions['L3']['TL1L2'] = self.TL1L2( kernel )
            contributions['L3']['TL2L3'] = self.TL2L3( kernel )

        contributions['DRAM'] = defaultdict(float)
        if self.TOL(kernel) > self.TnOL(kernel) + self.TL1L2(kernel) + self.TL2L3_datainDRAM(kernel) + self.TMem(kernel):
            contributions['DRAM']['core'], contributions['DRAM']['exp'] = self.core_rate_limiting_steps( kernel )
        else:
            contributions['DRAM']['Tload'] = self.TnOL( kernel )
            contributions['DRAM']['TL1L2'] = self.TL1L2( kernel )
            contributions['DRAM']['TL2L3'] = self.TL2L3( kernel )
            contributions['DRAM']['DRAM']  = self.TMem( kernel )

        return contributions










