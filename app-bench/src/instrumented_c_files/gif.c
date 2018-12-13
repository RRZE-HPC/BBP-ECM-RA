/* Created by Language version: 6.2.0 */
/* VECTORIZED */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "coreneuron/mech/cfile/scoplib.h"
#undef PI
#ifdef LIKWID_PERFMON
    #include "likwid.h"
#endif

#include "coreneuron/nrnoc/md1redef.h"
#include "coreneuron/nrnconf.h"
#include "coreneuron/nrnoc/multicore.h"

#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
#include "coreneuron/nrniv/nrn_acc_manager.h"

#endif
#include "coreneuron/utils/randoms/nrnran123.h"

#include "coreneuron/nrnoc/md2redef.h"
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#if !defined(DISABLE_HOC_EXP)
#undef exp
#define exp hoc_Exp
#endif
extern double hoc_Exp(double);
#endif
 
#define _thread_present_ /**/ , _slist1[0:6], _dlist1[0:6] 
 
#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
#include <openacc.h>
#if defined(PG_ACC_BUGS)
#define _PRAGMA_FOR_INIT_ACC_LOOP_ _Pragma("acc parallel loop present(_ni[0:_cntml_actual], _nt_data[0:_nt->_ndata], _p[0:_cntml_padded*_psize], _ppvar[0:_cntml_padded*_ppsize], _vec_v[0:_nt->end], nrn_ion_global_map[0:nrn_ion_global_map_size][0:3], _nt[0:1] _thread_present_) if(_nt->compute_gpu)")
#else
#define _PRAGMA_FOR_INIT_ACC_LOOP_ _Pragma("acc parallel loop present(_ni[0:_cntml_actual], _nt_data[0:_nt->_ndata], _p[0:_cntml_padded*_psize], _ppvar[0:_cntml_padded*_ppsize], _vec_v[0:_nt->end], nrn_ion_global_map[0:nrn_ion_global_map_size], _nt[0:1] _thread_present_) if(_nt->compute_gpu)")
#endif
#define _PRAGMA_FOR_STATE_ACC_LOOP_ _Pragma("acc parallel loop present(_ni[0:_cntml_actual], _nt_data[0:_nt->_ndata], _p[0:_cntml_padded*_psize], _ppvar[0:_cntml_padded*_ppsize], _vec_v[0:_nt->end], _nt[0:1], _ml[0:1] _thread_present_) if(_nt->compute_gpu) async(stream_id)")
#define _PRAGMA_FOR_CUR_ACC_LOOP_ _Pragma("acc parallel loop present(_ni[0:_cntml_actual], _nt_data[0:_nt->_ndata], _p[0:_cntml_padded*_psize], _ppvar[0:_cntml_padded*_ppsize], _vec_v[0:_nt->end], _vec_d[0:_nt->end], _vec_rhs[0:_nt->end], _nt[0:1] _thread_present_) if(_nt->compute_gpu) async(stream_id)")
#define _PRAGMA_FOR_CUR_SYN_ACC_LOOP_ _Pragma("acc parallel loop present(_ni[0:_cntml_actual], _nt_data[0:_nt->_ndata], _p[0:_cntml_padded*_psize], _ppvar[0:_cntml_padded*_ppsize], _vec_v[0:_nt->end], _vec_shadow_rhs[0:_nt->shadow_rhs_cnt], _vec_shadow_d[0:_nt->shadow_rhs_cnt], _vec_d[0:_nt->end], _vec_rhs[0:_nt->end], _nt[0:1]) if(_nt->compute_gpu) async(stream_id)")
#define _PRAGMA_FOR_NETRECV_ACC_LOOP_ _Pragma("acc parallel loop present(_pnt[0:_pnt_length], _nrb[0:1], _nt[0:1], nrn_threads[0:nrn_nthread]) if(_nt->compute_gpu) async(stream_id)")
#define _ACC_GLOBALS_UPDATE_ if (_nt->compute_gpu) {_acc_globals_update();}
#else
#define _PRAGMA_FOR_INIT_ACC_LOOP_ _Pragma("")
#define _PRAGMA_FOR_STATE_ACC_LOOP_ _Pragma("")
#define _PRAGMA_FOR_CUR_ACC_LOOP_ _Pragma("")
#define _PRAGMA_FOR_CUR_SYN_ACC_LOOP_ _Pragma("")
#define _PRAGMA_FOR_NETRECV_ACC_LOOP_ _Pragma("")
#define _ACC_GLOBALS_UPDATE_ ;
#endif
 
#if defined(__clang__)
#define _PRAGMA_FOR_VECTOR_LOOP_ _Pragma("clang loop vectorize(enable)")
#elif defined(__ICC) || defined(__INTEL_COMPILER)
#define _PRAGMA_FOR_VECTOR_LOOP_ _Pragma("ivdep")
#elif defined(__IBMC__) || defined(__IBMCPP__)
#define _PRAGMA_FOR_VECTOR_LOOP_ _Pragma("ibm independent_loop")
#elif defined(__PGI)
#define _PRAGMA_FOR_VECTOR_LOOP_ _Pragma("vector")
#elif defined(_CRAYC)
#define _PRAGMA_FOR_VECTOR_LOOP_ _Pragma("_CRI ivdep")
#elif defined(__GNUC__) || defined(__GNUG__)
#define _PRAGMA_FOR_VECTOR_LOOP_ _Pragma("GCC ivdep")
#else
#define _PRAGMA_FOR_VECTOR_LOOP_
#endif // _PRAGMA_FOR_VECTOR_LOOP_
 
#if !defined(LAYOUT)
/* 1 means AoS, >1 means AoSoA, <= 0 means SOA */
#define LAYOUT 1
#endif
#if LAYOUT >= 1
#define _STRIDE LAYOUT
#else
#define _STRIDE _cntml_padded + _iml
#endif
 

#if !defined(NET_RECEIVE_BUFFERING)
#define NET_RECEIVE_BUFFERING 1
#endif
 
#define nrn_init _nrn_init__GifCurrent
#define nrn_cur _nrn_cur__GifCurrent
#define _nrn_current _nrn_current__GifCurrent
#define nrn_jacob _nrn_jacob__GifCurrent
#define nrn_state _nrn_state__GifCurrent
#define initmodel initmodel__GifCurrent
#define _net_receive _net_receive__GifCurrent
#define nrn_state_launcher nrn_state_GifCurrent_launcher
#define nrn_cur_launcher nrn_cur_GifCurrent_launcher
#define nrn_jacob_launcher nrn_jacob_GifCurrent_launcher 
#if NET_RECEIVE_BUFFERING
#define _net_buf_receive _net_buf_receive_GifCurrent
static void _net_buf_receive(_NrnThread*);
#endif
 
#define _nrn_watch_check _nrn_watch_check__GifCurrent 
#define setRNG setRNG_GifCurrent 
#define states states_GifCurrent 
 
#define _threadargscomma_ _iml, _cntml_padded, _p, _ppvar, _thread, _nt, v,
#define _threadargsprotocomma_ int _iml, int _cntml_padded, double* _p, Datum* _ppvar, ThreadDatum* _thread, _NrnThread* _nt, double v,
#define _threadargs_ _iml, _cntml_padded, _p, _ppvar, _thread, _nt, v
#define _threadargsproto_ int _iml, int _cntml_padded, double* _p, Datum* _ppvar, ThreadDatum* _thread, _NrnThread* _nt, double v
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define Vr _p[0*_STRIDE]
#define Tref _p[1*_STRIDE]
#define Vt_star _p[2*_STRIDE]
#define DV _p[3*_STRIDE]
#define lambda0 _p[4*_STRIDE]
#define tau_eta1 _p[5*_STRIDE]
#define tau_eta2 _p[6*_STRIDE]
#define tau_eta3 _p[7*_STRIDE]
#define a_eta1 _p[8*_STRIDE]
#define a_eta2 _p[9*_STRIDE]
#define a_eta3 _p[10*_STRIDE]
#define tau_gamma1 _p[11*_STRIDE]
#define tau_gamma2 _p[12*_STRIDE]
#define tau_gamma3 _p[13*_STRIDE]
#define a_gamma1 _p[14*_STRIDE]
#define a_gamma2 _p[15*_STRIDE]
#define a_gamma3 _p[16*_STRIDE]
#define e_spike _p[17*_STRIDE]
#define i _p[18*_STRIDE]
#define i_eta _p[19*_STRIDE]
#define p_dontspike _p[20*_STRIDE]
#define rand _p[21*_STRIDE]
#define grefrac _p[22*_STRIDE]
#define gamma_sum _p[23*_STRIDE]
#define verboseLevel _p[24*_STRIDE]
#define isrefrac _p[25*_STRIDE]
#define eta1 _p[26*_STRIDE]
#define eta2 _p[27*_STRIDE]
#define eta3 _p[28*_STRIDE]
#define gamma1 _p[29*_STRIDE]
#define gamma2 _p[30*_STRIDE]
#define gamma3 _p[31*_STRIDE]
#define lambda _p[32*_STRIDE]
#define irefrac _p[33*_STRIDE]
#define Deta1 _p[34*_STRIDE]
#define Deta2 _p[35*_STRIDE]
#define Deta3 _p[36*_STRIDE]
#define Dgamma1 _p[37*_STRIDE]
#define Dgamma2 _p[38*_STRIDE]
#define Dgamma3 _p[39*_STRIDE]
#define _v_unused _p[40*_STRIDE]
#define _g_unused _p[41*_STRIDE]
#define _tsav _p[42*_STRIDE]
 
#ifndef NRN_PRCELLSTATE
#define NRN_PRCELLSTATE 0
#endif
#if NRN_PRCELLSTATE
#define _PRCELLSTATE_V _v_unused = _v;
#define _PRCELLSTATE_G _g_unused = _g;
#else
#define _PRCELLSTATE_V /**/
#define _PRCELLSTATE_G /**/
#endif
#define _nd_area  _nt_data[_ppvar[0*_STRIDE]]
#define _p_rng	_nt->_vdata[_ppvar[2*_STRIDE]]
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  2;
 static ThreadDatum* _extcall_thread;
 /* external NEURON variables */
 
#if 0 /*BBCORE*/
 /* declaration of user functions */
 static double _hoc_setRNG();
 static double _hoc_toggleVerbose();
 static double _hoc_urand();
 
#endif /*BBCORE*/
 
#define _mechtype _mechtype_GifCurrent
int _mechtype;
#pragma acc declare copyin (_mechtype)
 extern int nrn_get_mechtype();
extern void hoc_register_prop_size(int, int, int);
extern Memb_func* memb_func;
 static int _pointtype;
 
#if 0 /*BBCORE*/
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 
#endif /*BBCORE*/
 
#if 0 /*BBCORE*/
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 "setRNG", _hoc_setRNG,
 "toggleVerbose", _hoc_toggleVerbose,
 "urand", _hoc_urand,
 0, 0
};
 
#endif /*BBCORE*/
#define toggleVerbose toggleVerbose_GifCurrent
#define urand urand_GifCurrent
 inline double toggleVerbose( _threadargsproto_ );
 inline double urand( _threadargsproto_ );
 /* declare global and static user variables */
#define gon gon_GifCurrent
 double gon = 1e+06;
 #pragma acc declare copyin (gon)
 
static void _acc_globals_update() {
 #pragma acc update device (gon) if(nrn_threads->compute_gpu)
 }
 
#if 0 /*BBCORE*/
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gon_GifCurrent", "uS",
 "Vr", "mV",
 "Tref", "ms",
 "Vt_star", "mV",
 "DV", "mV",
 "lambda0", "Hz",
 "tau_eta1", "ms",
 "tau_eta2", "ms",
 "tau_eta3", "ms",
 "a_eta1", "nA",
 "a_eta2", "nA",
 "a_eta3", "nA",
 "tau_gamma1", "ms",
 "tau_gamma2", "ms",
 "tau_gamma3", "ms",
 "a_gamma1", "mV",
 "a_gamma2", "mV",
 "a_gamma3", "mV",
 "e_spike", "mV",
 "eta1", "nA",
 "eta2", "nA",
 "eta3", "nA",
 "gamma1", "mV",
 "gamma2", "mV",
 "gamma3", "mV",
 "i", "nA",
 "i_eta", "nA",
 "p_dontspike", "1",
 "rand", "1",
 "grefrac", "uS",
 "gamma_sum", "mV",
 "verboseLevel", "1",
 "isrefrac", "1",
 0,0
};
 
#endif /*BBCORE*/
 static double delta_t = 0.01;
 static double eta30 = 0;
 static double eta20 = 0;
 static double eta10 = 0;
 static double gamma30 = 0;
 static double gamma20 = 0;
 static double gamma10 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "gon_GifCurrent", &gon_GifCurrent,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void _ba1(_NrnThread*, _Memb_list*, int) ;
 static void nrn_alloc(double*, Datum*, int);
void nrn_init(_NrnThread*, _Memb_list*, int);
void nrn_state(_NrnThread*, _Memb_list*, int);
 void nrn_cur(_NrnThread*, _Memb_list*, int);
 void _nrn_watch_check(_NrnThread*, _Memb_list*);
 
#define _watch_array(arg) _ppvar[(arg + 4)*_STRIDE] 
 
#define _nrn_watch_activate(_item)\
  if (_watch_rm == 0) {\
    int _i;\
    for (_i = 1; _i < 2; ++_i) {\
      _watch_array(_i) = 0;\
    }\
    _watch_rm = 1;\
  }\
  _watch_array(_item) = 2 + 
#if 0 /*BBCORE*/
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   Prop* _prop = ((Point_process*)_vptr)->_prop;
   destroy_point_process(_vptr);
}
 
#endif /*BBCORE*/
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "6.2.0",
"GifCurrent",
 "Vr",
 "Tref",
 "Vt_star",
 "DV",
 "lambda0",
 "tau_eta1",
 "tau_eta2",
 "tau_eta3",
 "a_eta1",
 "a_eta2",
 "a_eta3",
 "tau_gamma1",
 "tau_gamma2",
 "tau_gamma3",
 "a_gamma1",
 "a_gamma2",
 "a_gamma3",
 "e_spike",
 0,
 "i",
 "i_eta",
 "p_dontspike",
 "rand",
 "grefrac",
 "gamma_sum",
 "verboseLevel",
 "isrefrac",
 0,
 "eta1",
 "eta2",
 "eta3",
 "gamma1",
 "gamma2",
 "gamma3",
 0,
 "rng",
 0};
 
static void nrn_alloc(double* _p, Datum* _ppvar, int _type) {
 
#if 0 /*BBCORE*/
 	/*initialize range parameters*/
 	Vr = -50;
 	Tref = 4;
 	Vt_star = -48;
 	DV = 0.5;
 	lambda0 = 1;
 	tau_eta1 = 1;
 	tau_eta2 = 10;
 	tau_eta3 = 100;
 	a_eta1 = 1;
 	a_eta2 = 1;
 	a_eta3 = 1;
 	tau_gamma1 = 1;
 	tau_gamma2 = 10;
 	tau_gamma3 = 100;
 	a_gamma1 = 1;
 	a_gamma2 = 1;
 	a_gamma3 = 1;
 	e_spike = 0;
 
#endif /* BBCORE */
 
}
 static void _initlists();
 
#define _tqitem &(_nt->_vdata[_ppvar[3*_STRIDE]])
 
#if NET_RECEIVE_BUFFERING
#undef _tqitem
#define _tqitem _ppvar[3*_STRIDE]
#endif

 static void _net_receive(Point_process*, int, double);
 
#define _psize 43
#define _ppsize 6
 static void bbcore_read(double *, int*, int*, int*, _threadargsproto_);
 extern void hoc_reg_bbcore_read(int, void(*)(double *, int*, int*, int*, _threadargsproto_));
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*f)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(_threadargsproto_, int));
extern void _cvode_abstol( Symbol**, double*, int);

 void _gif_reg() {
	int _vectorized = 1;
  _initlists();
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 if (_mechtype == -1) return;
 _nrn_layout_reg(_mechtype, LAYOUT);
 
#if 0 /*BBCORE*/
 
#endif /*BBCORE*/
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, NULL, nrn_state, nrn_init,
	 hoc_nrnpointerindex,
	 NULL/*_hoc_create_pnt*/, NULL/*_hoc_destroy_pnt*/, /*_member_func,*/
	 1);
   hoc_reg_bbcore_read(_mechtype, bbcore_read);
  hoc_register_prop_size(_mechtype, _psize, _ppsize);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "bbcorepointer");
  hoc_register_dparam_semantics(_mechtype, 3, "netsend");
  hoc_register_dparam_semantics(_mechtype, 4, "watch");
  hoc_register_dparam_semantics(_mechtype, 5, "watch");
 hoc_register_watch_check(_nrn_watch_check, _mechtype);
 
#if NET_RECEIVE_BUFFERING
  hoc_register_net_receive_buffering(_net_buf_receive, _mechtype);
#endif
 
#if NET_RECEIVE_BUFFERING
  hoc_register_net_send_buffering(_mechtype);
#endif
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_reg_ba(_mechtype, _ba1, 22);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, NULL);
 }
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int setRNG(_threadargsproto_);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 
#define _slist1 _slist1_GifCurrent
int* _slist1;
#pragma acc declare create(_slist1)

#define _dlist1 _dlist1_GifCurrent
int* _dlist1;
#pragma acc declare create(_dlist1)
 static inline int states(_threadargsproto_);
 
/*VERBATIM*/
#include "nrnran123.h"
 /* AFTER SOLVE */
 static void _ba1(_NrnThread* _nt, _Memb_list* _ml, int _type)  {
     double* _p; Datum* _ppvar; ThreadDatum* _thread;
  int* _ni; double v; int _iml, _cntml_padded, _cntml_actual;
  _cntml_actual = _ml->_nodecount;
  _cntml_padded = _ml->_nodecount_padded;
  _ni = _ml->_nodeindices;
  _thread = _ml->_thread;
  double * _nt_data = _nt->_data;
  double * _vec_v = _nt->_actual_v;
  int stream_id = _nt->stream_id;
  #if LAYOUT == 1 /*AoS*/
  for (_iml = 0; _iml < _cntml_actual; ++_iml) {
    _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
  #elif LAYOUT == 0 /*SoA*/
    _p = _ml->_data; _ppvar = _ml->_pdata;
  /* insert compiler dependent ivdep like pragma */
  _PRAGMA_FOR_VECTOR_LOOP_
  _PRAGMA_FOR_STATE_ACC_LOOP_
  for (_iml = 0; _iml < _cntml_actual; ++_iml) {
  #else /* LAYOUT > 1 */ /*AoSoA*/
  #error AoSoA not implemented.
  for (;;) { /* help clang-format properly indent */
  #endif
    v = _vec_v[_ni[_iml]];
 rand = urand ( _threadargs_ ) ;
   }
 }
 
/*CVODE*/
 static int _ode_spec1 (_threadargsproto_) {int _reset = 0; {
   Deta1 = - eta1 / tau_eta1 ;
   Deta2 = - eta2 / tau_eta2 ;
   Deta3 = - eta3 / tau_eta3 ;
   Dgamma1 = - gamma1 / tau_gamma1 ;
   Dgamma2 = - gamma2 / tau_gamma2 ;
   Dgamma3 = - gamma3 / tau_gamma3 ;
   }
 return _reset;
}
 static int _ode_matsol1 (_threadargsproto_) {
 Deta1 = Deta1  / (1. - dt*( ( - 1.0 ) / tau_eta1 )) ;
 Deta2 = Deta2  / (1. - dt*( ( - 1.0 ) / tau_eta2 )) ;
 Deta3 = Deta3  / (1. - dt*( ( - 1.0 ) / tau_eta3 )) ;
 Dgamma1 = Dgamma1  / (1. - dt*( ( - 1.0 ) / tau_gamma1 )) ;
 Dgamma2 = Dgamma2  / (1. - dt*( ( - 1.0 ) / tau_gamma2 )) ;
 Dgamma3 = Dgamma3  / (1. - dt*( ( - 1.0 ) / tau_gamma3 )) ;
 return 0;
}
 /*END CVODE*/
 static int states (_threadargsproto_) { {
    eta1 = eta1 + (1. - exp(dt*(( - 1.0 ) / tau_eta1)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_eta1 ) - eta1) ;
    eta2 = eta2 + (1. - exp(dt*(( - 1.0 ) / tau_eta2)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_eta2 ) - eta2) ;
    eta3 = eta3 + (1. - exp(dt*(( - 1.0 ) / tau_eta3)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_eta3 ) - eta3) ;
    gamma1 = gamma1 + (1. - exp(dt*(( - 1.0 ) / tau_gamma1)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_gamma1 ) - gamma1) ;
    gamma2 = gamma2 + (1. - exp(dt*(( - 1.0 ) / tau_gamma2)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_gamma2 ) - gamma2) ;
    gamma3 = gamma3 + (1. - exp(dt*(( - 1.0 ) / tau_gamma3)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_gamma3 ) - gamma3) ;
   }
  return 0;
}
 
#if NET_RECEIVE_BUFFERING 
#undef t
#define t _nrb_t
static void _net_receive_kernel(double, Point_process*, int _weight_index, double _flag);
static void _net_buf_receive(_NrnThread* _nt) {
  if (!_nt->_ml_list) { return; }
  _Memb_list* _ml = _nt->_ml_list[_mechtype];
  if (!_ml) { return; }
  NetReceiveBuffer_t* _nrb = _ml->_net_receive_buffer; 
  int _di;
  int stream_id = _nt->stream_id;
  Point_process* _pnt = _nt->pntprocs;
  int _pnt_length = _nt->n_pntproc - _nrb->_pnt_offset;
  int _displ_cnt = _nrb->_displ_cnt;
  _PRAGMA_FOR_NETRECV_ACC_LOOP_ 
  for (_di = 0; _di < _displ_cnt; ++_di) {
    int _inrb;
    int _di0 = _nrb->_displ[_di];
    int _di1 = _nrb->_displ[_di + 1];
    for (_inrb = _di0; _inrb < _di1; ++_inrb) {
      int _i = _nrb->_nrb_index[_inrb];
      int _j = _nrb->_pnt_index[_i];
      int _k = _nrb->_weight_index[_i];
      double _nrt = _nrb->_nrb_t[_i];
      double _nrflag = _nrb->_nrb_flag[_i];
      _net_receive_kernel(_nrt, _pnt + _j, _k, _nrflag);
    }
  }
  #pragma acc wait(stream_id)
  _nrb->_displ_cnt = 0;
  _nrb->_cnt = 0;
  /*printf("_net_buf_receive__GifCurrent  %d\n", _nt->_id);*/
 
  {
  NetSendBuffer_t* _nsb = _ml->_net_send_buffer;
#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
  #pragma acc update self(_nsb->_cnt) if(_nt->compute_gpu)
  update_net_send_buffer_on_host(_nt, _nsb);
#endif
  int _i;
  for (_i=0; _i < _nsb->_cnt; ++_i) {
    net_sem_from_gpu(_nsb->_sendtype[_i], _nsb->_vdata_index[_i],
      _nsb->_weight_index[_i], _nt->_id, _nsb->_pnt_index[_i],
      _nsb->_nsb_t[_i], _nsb->_nsb_flag[_i]);
  }
  _nsb->_cnt = 0;
#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
  #pragma acc update device(_nsb->_cnt) if (_nt->compute_gpu)
#endif
  }
 
}
 
static void _net_send_buffering(NetSendBuffer_t* _nsb, int _sendtype, int _i_vdata, int _weight_index,
 int _ipnt, double _t, double _flag) {
  int _i = 0;
  #pragma acc atomic capture
  _i = _nsb->_cnt++;
  if (_i >= _nsb->_size) {
  }
  _nsb->_sendtype[_i] = _sendtype;
  _nsb->_vdata_index[_i] = _i_vdata;
  _nsb->_weight_index[_i] = _weight_index;
  _nsb->_pnt_index[_i] = _ipnt;
  _nsb->_nsb_t[_i] = _t;
  _nsb->_nsb_flag[_i] = _flag;
}
 
static void _net_receive (Point_process* _pnt, int _weight_index, double _lflag) {
  _NrnThread* _nt = nrn_threads + _pnt->_tid;
  NetReceiveBuffer_t* _nrb = _nt->_ml_list[_mechtype]->_net_receive_buffer;
  if (_nrb->_cnt >= _nrb->_size){
    realloc_net_receive_buffer(_nt, _nt->_ml_list[_mechtype]);
  }
  _nrb->_pnt_index[_nrb->_cnt] = _pnt - _nt->pntprocs;
  _nrb->_weight_index[_nrb->_cnt] = _weight_index;
  _nrb->_nrb_t[_nrb->_cnt] = _nt->_t;
  _nrb->_nrb_flag[_nrb->_cnt] = _lflag;
  ++_nrb->_cnt;
}
 
static void _net_receive_kernel(double _nrb_t, Point_process* _pnt, int _weight_index, double _lflag)
#else
 
static void _net_receive (Point_process* _pnt, int _weight_index, double _lflag) 
#endif
 
{  double* _p; Datum* _ppvar; ThreadDatum* _thread; double v;
   _Memb_list* _ml; int _cntml_padded, _cntml_actual; int _iml; double* _args;
   int _watch_rm = 0;
 
   _NrnThread* _nt;
   int _tid = _pnt->_tid; 
   _nt = nrn_threads + _tid;
   _thread = (ThreadDatum*)0; 
   double *_weights = _nt->_weights;
   _args = _weights + _weight_index;
   _ml = _nt->_ml_list[_pnt->_type];
   _cntml_actual = _ml->_nodecount;
   _cntml_padded = _ml->_nodecount_padded;
   _iml = _pnt->_i_instance;
#if LAYOUT == 1 /*AoS*/
   _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
#endif
#if LAYOUT == 0 /*SoA*/
   _p = _ml->_data; _ppvar = _ml->_pdata;
#endif
#if LAYOUT > 1 /*AoSoA*/
#error AoSoA not implemented.
#endif
  #if !defined(_OPENACC) 
 assert(_tsav <= t); 
 #endif 
 _tsav = t;  v = VEC_V(_ml->_nodeindices[_iml]);
 
#if !NET_RECEIVE_BUFFERING
  if (_lflag == 1. ) {*(_tqitem) = 0;}
#endif
 {
   if ( _lflag  == 1.0 ) {
     isrefrac = 1.0 ;
     
#if NET_RECEIVE_BUFFERING
    _net_send_buffering(_ml->_net_send_buffer, 0, _tqitem, _weight_index, _ppvar[1*_STRIDE], t +  dt , 2.0 );
#else
 net_send ( _tqitem, _weight_index, _pnt, t +  dt , 2.0 ) ;
     
#endif
 if ( verboseLevel > 0.0 ) {
       printf ( "Next dt: spike, at time %g: rand=%g, p_dontspike=%g\n" , t , rand , p_dontspike ) ;
       }
     }
   else if ( _lflag  == 2.0 ) {
     v = 0.0 ;
     grefrac = gon ;
     
#if NET_RECEIVE_BUFFERING
    _net_send_buffering(_ml->_net_send_buffer, 0, _tqitem, _weight_index, _ppvar[1*_STRIDE], t +  Tref - dt , 3.0 );
#else
 net_send ( _tqitem, _weight_index, _pnt, t +  Tref - dt , 3.0 ) ;
     
#endif
 if ( verboseLevel > 0.0 ) {
       printf ( "Start spike, at time %g: rand=%g, p_dontspike=%g\n" , t , rand , p_dontspike ) ;
       }
     }
   else if ( _lflag  == 3.0 ) {
     v = Vr ;
     isrefrac = 0.0 ;
     grefrac = 0.0 ;
     eta1 = eta1 + a_eta1 ;
     eta2 = eta2 + a_eta2 ;
     eta3 = eta3 + a_eta3 ;
     gamma1 = gamma1 + a_gamma1 ;
     gamma2 = gamma2 + a_gamma2 ;
     gamma3 = gamma3 + a_gamma3 ;
     if ( verboseLevel > 0.0 ) {
       printf ( "End refrac, at time %g: rand=%g, p_dontspike=%g\n" , t , rand , p_dontspike ) ;
       }
     }
   else if ( _lflag  == 4.0 ) {
     _nrn_watch_activate(1)  ( rand > p_dontspike ) ; /* 1.0 */
 }
   } 
#if NET_RECEIVE_BUFFERING
#undef t
#define t _nt->_t
#endif
 
 VEC_V(_ml->_nodeindices[_iml]) = v;
 }
 
static int  setRNG ( _threadargsproto_ ) {
   
/*VERBATIM*/
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
  return 0; }
 
#if 0 /*BBCORE*/
 
static double _hoc_setRNG(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; ThreadDatum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r = 1.;
 setRNG ( _threadargs_ );
 return(_r);
}
 
#endif /*BBCORE*/
 
double urand ( _threadargsproto_ ) {
   double _lurand;
 
/*VERBATIM*/
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
 
return _lurand;
 }
 
#if 0 /*BBCORE*/
 
static double _hoc_urand(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; ThreadDatum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  urand ( _threadargs_ );
 return(_r);
}
 
#endif /*BBCORE*/
 
/*VERBATIM*/
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
 
double toggleVerbose ( _threadargsproto_ ) {
   double _ltoggleVerbose;
 verboseLevel = 1.0 - verboseLevel ;
   
return _ltoggleVerbose;
 }
 
#if 0 /*BBCORE*/
 
static double _hoc_toggleVerbose(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; ThreadDatum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  toggleVerbose ( _threadargs_ );
 return(_r);
}
 
#endif /*BBCORE*/
 
void _nrn_watch_check(_NrnThread* _nt, _Memb_list* _ml) {
  double* _p; Datum* _ppvar; ThreadDatum* _thread;
  int* _ni; double v; int _iml, _cntml_padded, _cntml_actual;
  _cntml_actual = _ml->_nodecount;
  _cntml_padded = _ml->_nodecount_padded;
  _ni = _ml->_nodeindices;
  _thread = _ml->_thread;
  double * _nt_data = _nt->_data;
  double * _vec_v = _nt->_actual_v;
  int stream_id = _nt->stream_id;
 
  #if LAYOUT == 1 /*AoS*/
  for (_iml = 0; _iml < _cntml_actual; ++_iml) {
    _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
  #elif LAYOUT == 0 /*SoA*/
    _p = _ml->_data; _ppvar = _ml->_pdata;
  /* insert compiler dependent ivdep like pragma */
  _PRAGMA_FOR_VECTOR_LOOP_
  _PRAGMA_FOR_STATE_ACC_LOOP_
  for (_iml = 0; _iml < _cntml_actual; ++_iml) {
  #else /* LAYOUT > 1 */ /*AoSoA*/
  #error AoSoA not implemented.
  for (;;) { /* help clang-format properly indent */
  #endif
    v = _vec_v[_ni[_iml]];
 
    if (_watch_array(1)&2) {
      if  ( rand > p_dontspike ) {
        if ((_watch_array(1)&1) == 0) {
          #if NET_RECEIVE_BUFFERING
          _net_send_buffering(_ml->_net_send_buffer, 0, _tqitem, 0, _ppvar[1*_STRIDE], t +  0.0 , 1.0 );
          #else
          net_send ( _tqitem, -1, _nt->_vdata[_ppvar[1*_STRIDE]], t +  0.0 , 1.0 ) ;
          #endif
        }
        _watch_array(1) = 3;
      }else{
        _watch_array(1) = 2;
      }
    }
   }
 
#if NET_RECEIVE_BUFFERING
  NetSendBuffer_t* _nsb = _ml->_net_send_buffer;
#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
  #pragma acc wait(stream_id)
  #pragma acc update self(_nsb->_cnt) if(_nt->compute_gpu)
  update_net_send_buffer_on_host(_nt, _nsb);
#endif
  {int _i;
  for (_i=0; _i < _nsb->_cnt; ++_i) {
    net_sem_from_gpu(_nsb->_sendtype[_i], _nsb->_vdata_index[_i],
      _nsb->_weight_index[_i], _nt->_id, _nsb->_pnt_index[_i],
      _nsb->_nsb_t[_i], _nsb->_nsb_flag[_i]);
  }}
  _nsb->_cnt = 0;
#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
  #pragma acc update device(_nsb->_cnt) if(_nt->compute_gpu)
#endif
#endif
 }

static void initmodel(_threadargsproto_) {
  int _i; double _save;{
  _Memb_list* _ml = _nt->_ml_list[_mechtype];
  eta3 = eta30;
  eta2 = eta20;
  eta1 = eta10;
  gamma3 = gamma30;
  gamma2 = gamma20;
  gamma1 = gamma10;
 {
   grefrac = 0.0 ;
   eta1 = 0.0 ;
   eta2 = 0.0 ;
   eta3 = 0.0 ;
   gamma1 = 0.0 ;
   gamma2 = 0.0 ;
   gamma3 = 0.0 ;
   rand = urand ( _threadargs_ ) ;
   p_dontspike = 2.0 ;
   isrefrac = 0.0 ;
   
#if NET_RECEIVE_BUFFERING
    _net_send_buffering(_ml->_net_send_buffer, 0, _tqitem, 0, _ppvar[1*_STRIDE], t +  0.0 , 4.0 );
#else
 net_send ( _tqitem, -1, _nt->_vdata[_ppvar[1*_STRIDE]], t +  0.0 , 4.0 ) ;
   
#endif
 }
 
}
}

void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; ThreadDatum* _thread;
double _v, v; int* _ni; int _iml, _cntml_padded, _cntml_actual;
    _ni = _ml->_nodeindices;
_cntml_actual = _ml->_nodecount;
_cntml_padded = _ml->_nodecount_padded;
_thread = _ml->_thread;
  #pragma acc update device (_mechtype) if(_nt->compute_gpu)

#if defined(PG_ACC_BUGS)
#if defined(celsius)
#undef celsius;
_celsius_ = celsius;
#pragma acc update device (_celsius_) if(_nt->compute_gpu)
#define celsius _celsius_
#endif
#endif
_ACC_GLOBALS_UPDATE_
double * _nt_data = _nt->_data;
double * _vec_v = _nt->_actual_v;
int stream_id = _nt->stream_id;
#if LAYOUT == 1 /*AoS*/
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
 _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
#elif LAYOUT == 0 /*SoA*/
 _p = _ml->_data; _ppvar = _ml->_pdata;
/* insert compiler dependent ivdep like pragma */
_PRAGMA_FOR_VECTOR_LOOP_
_PRAGMA_FOR_INIT_ACC_LOOP_
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
#else /* LAYOUT > 1 */ /*AoSoA*/
#error AoSoA not implemented.
for (;;) { /* help clang-format properly indent */
#endif
    int _nd_idx = _ni[_iml];
 _tsav = -1e20;
    _v = _vec_v[_nd_idx];
    _PRCELLSTATE_V
 v = _v;
 _PRCELLSTATE_V
 initmodel(_threadargs_);
}

#if NET_RECEIVE_BUFFERING
  NetSendBuffer_t* _nsb = _ml->_net_send_buffer;
#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
  #pragma acc wait(stream_id)
  #pragma acc update self(_nsb->_cnt) if(_nt->compute_gpu)
  update_net_send_buffer_on_host(_nt, _nsb);
#endif
  {int _i;
  for (_i=0; _i < _nsb->_cnt; ++_i) {
    net_sem_from_gpu(_nsb->_sendtype[_i], _nsb->_vdata_index[_i],
      _nsb->_weight_index[_i], _nt->_id, _nsb->_pnt_index[_i],
      _nsb->_nsb_t[_i], _nsb->_nsb_flag[_i]);
  }}
  _nsb->_cnt = 0;
#if defined(_OPENACC) && !defined(DISABLE_OPENACC)
  #pragma acc update device(_nsb->_cnt) if(_nt->compute_gpu)
#endif
#endif
}

#if defined(ENABLE_CUDA_INTERFACE) && defined(_OPENACC)
  void nrn_state_launcher(_NrnThread*, _Memb_list*, int, int);
  void nrn_jacob_launcher(_NrnThread*, _Memb_list*, int, int);
  void nrn_cur_launcher(_NrnThread*, _Memb_list*, int, int);
#endif


void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; ThreadDatum* _thread;
int* _ni; double _rhs, _g, _v, v; int _iml, _cntml_padded, _cntml_actual;
    _ni = _ml->_nodeindices;
_cntml_actual = _ml->_nodecount;
_cntml_padded = _ml->_nodecount_padded;
_thread = _ml->_thread;
double * _vec_rhs = _nt->_actual_rhs;
double * _vec_d = _nt->_actual_d;
double * _vec_shadow_rhs = _nt->_shadow_rhs;
double * _vec_shadow_d = _nt->_shadow_d;

#if defined(ENABLE_CUDA_INTERFACE) && defined(_OPENACC) && !defined(DISABLE_OPENACC)
  _NrnThread* d_nt = acc_deviceptr(_nt);
  _Memb_list* d_ml = acc_deviceptr(_ml);
  nrn_cur_launcher(d_nt, d_ml, _type, _cntml_actual);
  return;
#endif

double * _nt_data = _nt->_data;
double * _vec_v = _nt->_actual_v;
int stream_id = _nt->stream_id;
#if LAYOUT == 1 /*AoS*/
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
 _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
#elif LAYOUT == 0 /*SoA*/
 _p = _ml->_data; _ppvar = _ml->_pdata;
/* insert compiler dependent ivdep like pragma */
_PRAGMA_FOR_VECTOR_LOOP_
_PRAGMA_FOR_CUR_SYN_ACC_LOOP_
LIKWID_MARKER_START("GIF_current");
#pragma omp simd simdlen(2)
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
#else /* LAYOUT > 1 */ /*AoSoA*/
#error AoSoA not implemented.
for (;;) { /* help clang-format properly indent */
#endif
    int _nd_idx = _ni[_iml];
    _v = _vec_v[_nd_idx];
    _PRCELLSTATE_V
 {
 i_eta = eta1 + eta2 + eta3 ;
 gamma_sum = gamma1 + gamma2 + gamma3 ;
 lambda = lambda0 * exp ( ( _v - Vt_star - gamma_sum ) / DV ) ;
 if ( isrefrac > 0.0 ) {
   p_dontspike = 2.0 ;
   }
 else {
   p_dontspike = exp ( - lambda * ( dt * ( 1e-3 ) ) ) ;
   }
 irefrac = grefrac * ( _v - 0.0 ) ;
 i = irefrac + i_eta ;
  _rhs = i;
  _g = grefrac;
 }
 double _mfact =  1.e2/(_nd_area);
 _g *=  _mfact;
 _rhs *= _mfact;
 _PRCELLSTATE_G


#ifdef _OPENACC
  if(_nt->compute_gpu) {
    #pragma acc atomic update
    _vec_rhs[_nd_idx] -= _rhs;
    #pragma acc atomic update
    _vec_d[_nd_idx] += _g;
  } else {
    _vec_shadow_rhs[_iml] = _rhs;
    _vec_shadow_d[_iml] = _g;
  }
#else
  _vec_shadow_rhs[_iml] = _rhs;
  _vec_shadow_d[_iml] = _g;
#endif
 }
LIKWID_MARKER_STOP("GIF_current");
LIKWID_MARKER_START("GIF_reduction_cur");
#ifdef _OPENACC
    if(!(_nt->compute_gpu)) { 
        for (_iml = 0; _iml < _cntml_actual; ++_iml) {
           int _nd_idx = _ni[_iml];
           _vec_rhs[_nd_idx] -= _vec_shadow_rhs[_iml];
           _vec_d[_nd_idx] += _vec_shadow_d[_iml];
        }
#else
 for (_iml = 0; _iml < _cntml_actual; ++_iml) {
   int _nd_idx = _ni[_iml];
   _vec_rhs[_nd_idx] -= _vec_shadow_rhs[_iml];
   _vec_d[_nd_idx] += _vec_shadow_d[_iml];
#endif
 
}
 
LIKWID_MARKER_STOP("GIF_reduction_cur");
}

void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; ThreadDatum* _thread;
double v, _v = 0.0; int* _ni; int _iml, _cntml_padded, _cntml_actual;
    _ni = _ml->_nodeindices;
_cntml_actual = _ml->_nodecount;
_cntml_padded = _ml->_nodecount_padded;
_thread = _ml->_thread;

#if defined(ENABLE_CUDA_INTERFACE) && defined(_OPENACC) && !defined(DISABLE_OPENACC)
  _NrnThread* d_nt = acc_deviceptr(_nt);
  _Memb_list* d_ml = acc_deviceptr(_ml);
  nrn_state_launcher(d_nt, d_ml, _type, _cntml_actual);
  return;
#endif

double * _nt_data = _nt->_data;
double * _vec_v = _nt->_actual_v;
int stream_id = _nt->stream_id;
#if LAYOUT == 1 /*AoS*/
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
 _p = _ml->_data + _iml*_psize; _ppvar = _ml->_pdata + _iml*_ppsize;
#elif LAYOUT == 0 /*SoA*/
 _p = _ml->_data; _ppvar = _ml->_pdata;
/* insert compiler dependent ivdep like pragma */
_PRAGMA_FOR_VECTOR_LOOP_
_PRAGMA_FOR_STATE_ACC_LOOP_
LIKWID_MARKER_START("GIF_state");
#pragma omp simd simdlen(2)
for (_iml = 0; _iml < _cntml_actual; ++_iml) {
#else /* LAYOUT > 1 */ /*AoSoA*/
#error AoSoA not implemented.
for (;;) { /* help clang-format properly indent */
#endif
    int _nd_idx = _ni[_iml];
    _v = _vec_v[_nd_idx];
    _PRCELLSTATE_V
 v=_v;
{
 {   ///states(_threadargs_);
    eta1 = eta1 + (1. - exp(dt*(( - 1.0 ) / tau_eta1)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_eta1 ) - eta1) ;
    eta2 = eta2 + (1. - exp(dt*(( - 1.0 ) / tau_eta2)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_eta2 ) - eta2) ;
    eta3 = eta3 + (1. - exp(dt*(( - 1.0 ) / tau_eta3)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_eta3 ) - eta3) ;
    gamma1 = gamma1 + (1. - exp(dt*(( - 1.0 ) / tau_gamma1)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_gamma1 ) - gamma1) ;
    gamma2 = gamma2 + (1. - exp(dt*(( - 1.0 ) / tau_gamma2)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_gamma2 ) - gamma2) ;
    gamma3 = gamma3 + (1. - exp(dt*(( - 1.0 ) / tau_gamma3)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_gamma3 ) - gamma3) ;
  }}}

LIKWID_MARKER_STOP("GIF_state");
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
 int _cntml_actual=1;
 int _cntml_padded=1;
 int _iml=0;
  if (!_first) return;
 
 _slist1 = (int*)malloc(sizeof(int)*6);
 _dlist1 = (int*)malloc(sizeof(int)*6);
 _slist1[0] = &(eta1) - _p;  _dlist1[0] = &(Deta1) - _p;
 _slist1[1] = &(eta2) - _p;  _dlist1[1] = &(Deta2) - _p;
 _slist1[2] = &(eta3) - _p;  _dlist1[2] = &(Deta3) - _p;
 _slist1[3] = &(gamma1) - _p;  _dlist1[3] = &(Dgamma1) - _p;
 _slist1[4] = &(gamma2) - _p;  _dlist1[4] = &(Dgamma2) - _p;
 _slist1[5] = &(gamma3) - _p;  _dlist1[5] = &(Dgamma3) - _p;
 #pragma acc enter data copyin(_slist1[0:6])
 #pragma acc enter data copyin(_dlist1[0:6])

_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif
