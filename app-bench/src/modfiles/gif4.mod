NEURON {
	ARTIFICIAL_CELL Gif4
	RANGE v_l, v_e, v_i, v_rest, v_thresh, t_ref
    RANGE t0, v_mem, t_last_sp
    RANGE inv_tau_mem_e, inv_tau_mem_i
    RANGE inv_tau_e, inv_tau_i, inv_tau_l
    RANGE inv_delta_tau_mem_e, inv_delta_tau_mem_i
    RANGE min_net_delay, gid
}

PARAMETER {
    v_l
    v_e
    v_i
    v_rest
    v_thresh
    t_ref
    inv_tau_e
    inv_tau_i
    inv_tau_l
    inv_delta_tau_mem_e
    inv_delta_tau_mem_i
    min_net_delay
    gid
}

ASSIGNED {
    v_mem
    t0
    t_last_sp
    inv_tau_mem_e
    inv_tau_mem_i
}

PROCEDURE update_taus(d(ms)) {
    inv_tau_mem_e = inv_tau_mem_e*exp(-d*inv_tau_e)
    inv_tau_mem_i = inv_tau_mem_i*exp(-d*inv_tau_i)
}

PROCEDURE update_v(d(ms)) {
    LOCAL accumul_v, sum_of_inverse_time_constants, exp_factor, exc_contr, inh_contr

    sum_of_inverse_time_constants = inv_tau_l + inv_tau_mem_e + inv_tau_mem_i
    exp_factor = exp( -d*(sum_of_inverse_time_constants) )
    accumul_v = v_l
    accumul_v = accumul_v + ( v_mem - v_l )*exp_factor
    exc_contr = ( v_e - v_l  )*inv_tau_mem_e/( sum_of_inverse_time_constants - inv_tau_e  )
    exc_contr = exc_contr*( exp(-d*inv_tau_e) - exp_factor  )
    accumul_v = accumul_v + exc_contr
    inh_contr = ( v_i - v_l  )*inv_tau_mem_i/( sum_of_inverse_time_constants - inv_tau_i  )
    inh_contr = inh_contr*( exp(-d*inv_tau_i) - exp_factor  )
:    printf("update_v: exc_contr=%g, inh_contr=%g\n", exc_contr, inh_contr)
    v_mem = accumul_v + inh_contr
}

INITIAL {
	t0 = t
    t_last_sp = -1000.
    inv_tau_mem_e = 0.
    inv_tau_mem_i = 0.
    v_mem = v_rest
    net_send(min_net_delay, 1)
}

NET_RECEIVE (w) {
    LOCAL T, max_EPSP_amplitude, t_sp, v_old
:    printf("%g :: event %g t=%g t0=%g 1/tau_m_e=%g\n", gid, flag, t, t0, inv_tau_mem_e)

    if ( flag == 1 ) {
        update_taus( t-t0 )
        if ( t - t_last_sp > t_ref ) {
            v_old = v_mem
            update_v(t-t0)
            if ( v_mem > v_thresh ) {
                t_last_sp = t0 + (v_thresh - v_old)*(t - t0)/(v_mem - v_old)
:                printf("t=%g, gid=%g >> spike detected at time %g, v_mem=%g, v_old=%g\n", t, gid, t_last_sp, v_mem, v_old)
                net_event( t_last_sp )
                :net_event( t )
            }
        } else {
:            printf("t=%g, I am refractory since %g\n", t, t_last_sp)
            v_mem = v_rest
        }
        net_send(min_net_delay, 1)

    } else {

        update_taus( t-t0 )
        if ( t - t_last_sp > t_ref ) {
            v_old = v_mem
            update_v(t-t0)
            if ( v_mem > v_thresh ) {
                t_last_sp = t0 + (v_thresh - v_old)*(t - t0)/(v_mem - v_old)
:                printf("t=%g, gid=%g >> spike detected at time %g, v_mem=%g, v_old=%g\n", t, gid, t_last_sp, v_mem, v_old)
                net_event( t_last_sp )
                :net_event( t )
            }
        } else {
:            printf("t=%g, I am refractory since %g\n", t, t_last_sp)
            v_mem = v_rest
        }

        if ( w > 0 ) {
            inv_tau_mem_e = inv_tau_mem_e + w*inv_delta_tau_mem_e
        } else {
            inv_tau_mem_i = inv_tau_mem_i - w*inv_delta_tau_mem_i
        }
:        printf("updated weights: inv_tau_mem_e=%g, inv_tau_mem_i=%g\n", inv_tau_mem_e, inv_tau_mem_i)
    }

    t0 = t
}
