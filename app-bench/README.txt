# INSTRUCTIONS FOR COMPILING

See README.txt inside src/ folder


# INSTRUCTIONS FOR RUNNING BENCHMARK

# 0. (Once) Update some paths inside the submit_all.py script

# 1. To submit the benchmark for current and state kernels:

$ python submit_all.py -d <PATH-TO>/app-bench/coredat/bench_ECM_theoretical_L5_TTPC1_500cells_500cellspergroup_f1Hz

# 2. To submit the benchmark for linear algebra:
$ python submit_all.py -d <PATH-TO>/app-bench/coredat/bench_ECM_theoretical_L5_TTPC1_linalg_15000cells -v AVX

# 3. To submit the benchmark for spike delivery:

## a. worst-case:
$ python submit_all.py -d <PATH-TO>/app-bench/coredat/spk_del_L5_TTPC1_rndDendTrgt_40000Hz_400000syns_per_cells6400000syns_active_per_step --binq --weak-scaling -v AVX

## b. best-case:
$ python submit_all.py -d <PATH-TO>/app-bench/coredat/spk_del_L5_TTPC1_bestCase_20000Hz_267syns_per_cells10000syns_active_per_step --binq --weak-scaling -v AVX

# 4. To submit the synthetic benchmarks

## a. See the src/ folder on how to compile an executable for synthetic benchmarks

## b. specify correct data folder in script:
$ python submit_all.py -d <PATH-TO>/app-bench/coredat/bench_ECM_theoretical_L5_TTPC1_DetAMPANMDA_1cells_1cellspergroup_f0Hz_L3 

# 5. Additional options for selecting number of threads, vectorization, number of runs, etc.
$ python submit_all.py --help
