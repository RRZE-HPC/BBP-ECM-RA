NEURON {
	POINT_PROCESS IAF_PSC_ALPHA
    RANGE P11_ex_
    RANGE P21_ex_
    RANGE P22_ex_
    RANGE P31_ex_
    RANGE P32_ex_
    RANGE P11_in_
    RANGE P21_in_
    RANGE P22_in_
    RANGE P31_in_
    RANGE P32_in_
    RANGE P33_
    RANGE expm1_tau_m_
    RANGE V_m
    RANGE dI_ex
    RANGE I_ex
    RANGE dI_in
    RANGE I_in
    RANGE v_rest
    RANGE t_ref
    RANGE v_thresh
    RANGE weighted_spikes_ex_
    RANGE weighted_spikes_in_
    RANGE EPSCInitialValue_
    RANGE IPSCInitialValue_
    RANGE i
    RANGE refractory
    NONSPECIFIC_CURRENT i
}

ASSIGNED {
    i
    V_m
    dI_ex
    I_ex
    dI_in
    I_in
    refractory
}

STATE {
:    V_m
:    dI_ex
:    I_ex
:    dI_in
:    I_in
}

PARAMETER {
    P11_ex_
    P21_ex_
    P22_ex_
    P31_ex_
    P32_ex_
    P11_in_
    P21_in_
    P22_in_
    P31_in_
    P32_in_
    P33_
    expm1_tau_m_
    v_rest
    refrac_counts
    v_thresh
    weighted_spikes_ex_
    weighted_spikes_in_
    EPSCInitialValue_
    IPSCInitialValue_
}

INITIAL {
    LOCAL tau_ex, tau_in, tau_m, C, denomin, t_ref
    tau_ex = 0.32582722403722841
    tau_in = 0.32582722403722841
    tau_m = 10.0
    C = 250.0
    t_ref = 0.5

    P11_ex_ = exp( -dt/tau_ex )
    P22_ex_ = exp( -dt/tau_ex )
    P11_in_ = exp( -dt/tau_in )
    P22_in_ = exp( -dt/tau_in )
    P33_ = exp( -dt/tau_m )
    expm1_tau_m_ = P33_ - 1.
    P21_ex_ = dt*P11_ex_
    P21_in_ = dt*P11_in_

    denomin = 1./tau_ex - 1./tau_m
    P31_ex_ = (1./C)*((P33_-P11_ex_)/(denomin*denomin) - dt*P11_ex_/denomin)
    P32_ex_ = (1./C)*(P33_-P11_ex_)/denomin

    denomin = 1./tau_in - 1./tau_m
    P31_in_ = (1./C)*((P33_-P11_in_)/(denomin*denomin) - dt*P11_in_/denomin)
    P32_in_ = (1./C)*(P33_-P11_in_)/denomin

    weighted_spikes_ex_ = 0.
    weighted_spikes_in_ = 0.
    EPSCInitialValue_ = 2.718281/tau_ex
    IPSCInitialValue_ = 2.718281/tau_in

    refrac_counts = floor( t_ref/dt )

    V_m = 5.7
    I_ex = 0.
    dI_ex = 0.
    I_in = 0.
    dI_in = 0.
    refractory = 0
    v_thresh = 20.0
    v_rest = 0.
}

PROCEDURE state() {

    if ( refractory > 0 ) {
        refractory = refractory - 1
    } else {
        V_m = P31_ex_*dI_ex + P32_ex_*I_ex + P31_in_*dI_in + P32_in_*I_in + expm1_tau_m_*V_m + V_m
    }

    I_ex = P21_ex_*dI_ex + P22_ex_*I_ex
    dI_ex = dI_ex*P11_ex_

    I_in = P21_in_*dI_in + P22_in_*I_in
    dI_in = dI_in*P11_in_

    dI_ex = dI_ex + EPSCInitialValue_*weighted_spikes_ex_
    weighted_spikes_ex_ = 0.

    dI_in = dI_in + IPSCInitialValue_*weighted_spikes_in_
    weighted_spikes_in_ = 0.

    : threshold crossing
    if ( V_m >= v_thresh ) {
        refractory = refrac_counts
        V_m = v_rest
    }
}

BREAKPOINT {
    LOCAL fake_g
    CONDUCTANCE fake_g
    SOLVE state
    i = 0.
    fake_g = 0.
}

NET_RECEIVE (weight) {
    if ( weight > 0. ) {
        weighted_spikes_ex_ = weighted_spikes_ex_ + weight
    } else {
        weighted_spikes_in_ = weighted_spikes_in_ + weight
    }
}





