class NaTs2_t():
    n_state_vars =  13
    n_params =  1
    def __init__(self):
        self.current = dict(
                name = 'NaTs2_t current',
                reads  = 6.5,
                writes = 6.,
                iaca_Thruput = {
                    "IVB.SSE": 8.4,
                    "IVB.AVX": 28,
                    "SKX.SSE": 8.6,
                    "SKX.AVX": 8.2,
                    "SKX.AVX512": 5.5},
                iaca_Tload = {
                    "IVB.SSE": 6,
                    "IVB.AVX": 6,
                    "SKX.SSE": 6,
                    "SKX.AVX": 5.4,
                    "SKX.AVX512": 3.1},
                nexp = 0
                )
        self.state = dict(
                name = 'NaTs2_t state',
                reads  = 1.5,
                writes = 10.,
                iaca_Thruput = {
                    "IVB.SSE": 140,
                    "IVB.AVX": 140,
                    "SKX.SSE": 39.8,
                    "SKX.AVX": 40,
                    "SKX.AVX512": 14.8},
                iaca_Tload = {
                    "IVB.SSE": 10.75,
                    "IVB.AVX": 8.5,
                    "SKX.SSE": 12.3,
                    "SKX.AVX": 7.5,
                    "SKX.AVX512": 3.7},
                iaca_CP = {
                    "IVB.SSE": 327./2.,
                    "IVB.AVX": 632./4.,
                    "SKX.SSE": 327./2.,
                    "SKX.AVX": 633./4.,
                    "SKX.AVX512": 633./4.}, # for the moment, since I don't have the info
                nexp = 7 # approx pow with exp
                )

class Ih():
    n_state_vars =  7
    n_params =  1
    def __init__(self):
        self.current = dict(
                name = 'Ih current',
                reads  = 3.5,
                writes = 4,
                iaca_Thruput = {
                    "IVB.SSE": 4.7,
                    "IVB.AVX": 4.7,
                    "SKX.SSE": 4.95,
                    "SKX.AVX": 6.,
                    "SKX.AVX512": 3.5},
                iaca_Tload = {
                    "IVB.SSE": 2.5,
                    "IVB.AVX": 3.,
                    "SKX.SSE": 2.5,
                    "SKX.AVX": 3.25,
                    "SKX.AVX512": 1.75},
                nexp = 0
                )
        self.state = dict(
                name = 'Ih state',
                reads  = 1.5,
                writes = 5,
                iaca_Thruput = {
                    "IVB.SSE": 56.,
                    "IVB.AVX": 56.,
                    "SKX.SSE": 16.,
                    "SKX.AVX": 15.9,
                    "SKX.AVX512": 7.6},
                iaca_Tload = {
                    "IVB.SSE": 4.5,
                    "IVB.AVX": 4.5,
                    "SKX.SSE": 6.,
                    "SKX.AVX": 3.4,
                    "SKX.AVX512": 1.9},
                iaca_CP = {
                    "IVB.SSE": 150./2.,
                    "IVB.AVX": 310./4.,
                    "SKX.SSE": 150./2.,
                    "SKX.AVX": 311./4.,
                    "SKX.AVX512": 311./4.},
                nexp = 3
                )

class Im():
    n_state_vars =  8
    n_params =  1
    def __init__(self):
        self.current = dict(
                name = 'Im current',
                reads  = 4.0 + 2*0.5,
                writes = 6.,
                iaca_Thruput = {
                    "IVB.SSE": 7.8,
                    "IVB.AVX": 7.8,
                    "SKX.SSE": 7.8,
                    "SKX.AVX": 7.3,
                    "SKX.AVX512": 5.3},
                iaca_Tload = {
                    "IVB.SSE": 5.5,
                    "IVB.AVX": 5.6,
                    "SKX.SSE": 5.5,
                    "SKX.AVX": 4.8,
                    "SKX.AVX512": 3.},
                nexp = 0
                )
        self.state = dict(
                name = 'Im state',
                reads  = 1.5,
                writes = 5.,
                iaca_Thruput = {
                    "IVB.SSE": 42.,
                    "IVB.AVX": 42.,
                    "SKX.SSE": 11.8,
                    "SKX.AVX": 11.9,
                    "SKX.AVX512": 6.6},
                iaca_Tload = {
                    "IVB.SSE": 4.5,
                    "IVB.AVX": 3.6,
                    "SKX.SSE": 6.,
                    "SKX.AVX": 5.8,
                    "SKX.AVX512": 1.8},
                iaca_CP = {
                    "IVB.SSE": 133./2.,
                    "IVB.AVX": 280./4.,
                    "SKX.SSE": 133./2.,
                    "SKX.AVX": 279./4.,
                    "SKX.AVX512": 279./4.},
                nexp = 4 # approx pow with exp
                )

class SKv3_1():
    n_state_vars =  6
    n_params =  1
    def __init__(self):
        self.current = dict(
                name = 'SKv3_1 current',
                reads  = 5.5,
                writes = 6.,
                iaca_Thruput = {
                    "IVB.SSE": 7.8,
                    "IVB.AVX": 7.8,
                    "SKX.SSE": 7.8,
                    "SKX.AVX": 8.8,
                    "SKX.AVX512": 5.3},
                iaca_Tload = {
                    "IVB.SSE": 5.5,
                    "IVB.AVX": 5.7,
                    "SKX.SSE": 5.5,
                    "SKX.AVX": 5.8,
                    "SKX.AVX512": 3.},
                nexp = 0
                )
        self.state = dict(
                name = 'SKv3_1 state',
                reads  = 1.5,
                writes = 3.,
                iaca_Thruput = {
                    "IVB.SSE": 49.,
                    "IVB.AVX": 49.,
                    "SKX.SSE": 13.9,
                    "SKX.AVX": 14.,
                    "SKX.AVX512": 11.6},
                iaca_Tload = {
                    "IVB.SSE": 3.3,
                    "IVB.AVX": 3.,
                    "SKX.SSE": 4.,
                    "SKX.AVX": 2.8,
                    "SKX.AVX512": 1.5},
                iaca_CP = {
                    "IVB.SSE": 138./2.,
                    "IVB.AVX": 286./4.,
                    "SKX.SSE": 138./2.,
                    "SKX.AVX": 287./4.,
                    "SKX.AVX512": 287./4.},
                nexp = 3
                )

#class ion():
#    def __init__(self):
#        self.current = dict(
#                name = 'ion current',
#                reads  = ,
#                writes = ,
#                iaca_Thruput = {
#                    "IVB.SSE": ,
#                    "IVB.AVX": ,
#                    "SKX.SSE": ,
#                    "SKX.AVX": ,
#                    "SKX.AVX512": },
#                iaca_Tload = {
#                    "IVB.SSE": ,
#                    "IVB.AVX": ,
#                    "SKX.SSE": ,
#                    "SKX.AVX": ,
#                    "SKX.AVX512": },
#                nexp = 
#                )
#        self.state = dict(
#                name = 'ion state',
#                reads  = ,
#                writes = ,
#                iaca_Thruput = {
#                    "IVB.SSE": ,
#                    "IVB.AVX": ,
#                    "SKX.SSE": ,
#                    "SKX.AVX": ,
#                    "SKX.AVX512": },
#                iaca_Tload = {
#                    "IVB.SSE": ,
#                    "IVB.AVX": ,
#                    "SKX.SSE": ,
#                    "SKX.AVX": ,
#                    "SKX.AVX512": },
#                nexp = 
#                )
#
