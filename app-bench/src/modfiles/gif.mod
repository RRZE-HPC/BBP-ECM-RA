: Generalized Integrate and Fire model defined in Pozzorini et al. PLOS Comp. Biol. 2015
: Filter for eta and gamma defined as linear combination of three exponential functions each.
:
: Implemented by Christian Roessert, EPFL/Blue Brain Project, 2016


NEURON {
    THREADSAFE
    POINT_PROCESS GifCurrent
    RANGE Vr, Tref, Vt_star
    RANGE DV, lambda0
    RANGE tau_eta1, tau_eta2, tau_eta3, a_eta1, a_eta2, a_eta3
    RANGE tau_gamma1, tau_gamma2, tau_gamma3, a_gamma1, a_gamma2, a_gamma3
    RANGE i_eta, gamma_sum, verboseLevel, p_dontspike, rand
    RANGE e_spike, isrefrac
    BBCOREPOINTER rng
    NONSPECIFIC_CURRENT i
}

UNITS {
    (mV) = (millivolt)
    (nA) = (nanoamp)
    (uS) = (microsiemens)
}

PARAMETER {
    Vr = -50 (mV)
    Tref = 4.0 (ms)
    Vt_star = -48 (mV)
    DV = 0.5 (mV)
    lambda0 = 1.0 (Hz)

    tau_eta1 = 1 (ms)
    tau_eta2 = 10. (ms)
    tau_eta3 = 100. (ms)
    a_eta1 = 1. (nA)
    a_eta2 = 1. (nA)
    a_eta3 = 1. (nA)

    tau_gamma1 = 1 (ms)
    tau_gamma2 = 10. (ms)
    tau_gamma3 = 100. (ms)
    a_gamma1 = 1. (mV)
    a_gamma2 = 1. (mV)
    a_gamma3 = 1. (mV)

    gon = 1e6 (uS)    : refractory clamp conductance
    e_spike = 0 (mV)  : spike height
}

COMMENT
The Verbatim block is needed to allow RNG.
ENDCOMMENT

VERBATIM
#include "nrnran123.h"
ENDVERBATIM

ASSIGNED {
    v (mV)
    i (nA)
    i_eta (nA)
    p_dontspike (1)
    lambda (Hz)
    irefrac (nA)
    rand (1)
    grefrac (uS)
    gamma_sum (mV)
    verboseLevel (1)
    dt (ms)
    rng
    isrefrac (1) : is in refractory period
}

STATE {
    eta1  (nA)
    eta2  (nA)
    eta3  (nA)
    gamma1  (mV)
    gamma2  (mV)
    gamma3  (mV)
}

INITIAL {
    grefrac = 0
    eta1 = 0
    eta2 = 0
    eta3 = 0
    gamma1 = 0
    gamma2 = 0
    gamma3 = 0
    rand = urand()
    p_dontspike = 2
    isrefrac = 0
    net_send(0,4)
}

BREAKPOINT {
    SOLVE states METHOD cnexp :derivimplicit :euler

    i_eta = eta1 + eta2 + eta3

    gamma_sum = gamma1 + gamma2 + gamma3
    lambda = lambda0*exp( (v-Vt_star-gamma_sum)/DV )
    if (isrefrac > 0) {
        p_dontspike = 2   : is in refractory period, make it impossible to trigger a spike
    } else {
        p_dontspike = exp(-lambda*(dt * (1e-3)))
    }

    irefrac = grefrac*(v-0)
    i = irefrac + i_eta

}

AFTER SOLVE {
    rand = urand()
}

DERIVATIVE states {     : solve spike frequency adaptation and spike triggered current kernels
    eta1' = -eta1/tau_eta1
    eta2' = -eta2/tau_eta2
    eta3' = -eta3/tau_eta3
    gamma1' = -gamma1/tau_gamma1
    gamma2' = -gamma2/tau_gamma2
    gamma3' = -gamma3/tau_gamma3
}

NET_RECEIVE (weight) {
    if (flag == 1) { : start spike next dt
        isrefrac = 1
        net_send(dt, 2)

        if( verboseLevel > 0 ) {
            printf("Next dt: spike, at time %g: rand=%g, p_dontspike=%g\n", t, rand, p_dontspike)
        }

    } else if (flag == 2) { : beginning of spike
        v = 0
        grefrac = gon
        net_send(Tref-dt, 3)
        :net_event(t)

        if( verboseLevel > 0 ) {
            printf("Start spike, at time %g: rand=%g, p_dontspike=%g\n", t, rand, p_dontspike)
        }

    } else if (flag == 3) { : end of refractory period
        v = Vr
        isrefrac = 0
        grefrac = 0

        : increase filters after refractory period
        eta1 = eta1 + a_eta1
        eta2 = eta2 + a_eta2
        eta3 = eta3 + a_eta3
        gamma1 = gamma1 + a_gamma1
        gamma2 = gamma2 + a_gamma2
        gamma3 = gamma3 + a_gamma3

        if( verboseLevel > 0 ) {
            printf("End refrac, at time %g: rand=%g, p_dontspike=%g\n", t, rand, p_dontspike)
        }

    } else if (flag == 4) { : watch for spikes
        WATCH (rand>p_dontspike) 1
    }
}

PROCEDURE setRNG() {
VERBATIM
    {
#if !NRNBBCORE
	nrnran123_State** pv = (nrnran123_State**)(&_p_rng);
	if (*pv) {
		nrnran123_deletestream(*pv);
		*pv = (nrnran123_State*)0;
	} 
	if (ifarg(2)) {
		*pv = nrnran123_newstream((uint32_t)*getarg(1), (uint32_t)*getarg(2));
	}
#endif
    }
ENDVERBATIM
}

FUNCTION urand() {
VERBATIM
	double value;
	if (_p_rng) {
		/*
		:Supports separate independent but reproducible streams for
		: each instance.
		*/
		value = nrnran123_negexp((nrnran123_State*)_p_rng);
		//printf("random stream for this simulation = %lf\n",value);
		return value;
	}else{
	        value = 0.0;
//		assert(0);
	}
	_lurand = value;
ENDVERBATIM
}

VERBATIM
static void bbcore_write(double* x, int* d, int* xx, int* offset, _threadargsproto_) {
	if (d) {
		uint32_t* di = ((uint32_t*)d) + *offset;
		nrnran123_State** pv = (nrnran123_State**)(&_p_rng);
		nrnran123_getids(*pv, di, di+1);
//printf("ProbAMPANMDA_EMS bbcore_write %d %d\n", di[0], di[1]);
	}
	*offset += 2;
}
static void bbcore_read(double* x, int* d, int* xx, int* offset, _threadargsproto_) {
	assert(!_p_rng);
	uint32_t* di = ((uint32_t*)d) + *offset;
        if (di[0] != 0 || di[1] != 0)
        {
	  nrnran123_State** pv = (nrnran123_State**)(&_p_rng);
	  *pv = nrnran123_newstream(di[0], di[1]);
        }
//printf("ProbAMPANMDA_EMS bbcore_read %d %d\n", di[0], di[1]);
	*offset += 2;
}
ENDVERBATIM


FUNCTION toggleVerbose() {
    verboseLevel = 1-verboseLevel
}
