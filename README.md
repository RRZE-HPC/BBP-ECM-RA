# BBP-ECM-RA
Reproducibility appendix for paper on modeling Blue Brain Project kernels with ECM

### To reproduce the figures using data from existing benchmarks

The output of benchmarks used as dataset in the paper is provided in the `results` folder.
To reproduce the figures, navigate to the `figures-and-tables` folder and simply execute the python scripts with the same name as the figure number.
The default parameters are already set to exactly match the required datasets from the `results` folder, but you may call the `--help` option to get an idea of which datasets are being used.

### To reproduce the tables using data from existing benchmarks

Again, the raw data is stored in the `results` folder.
To reproduce the tables, first you must navigate to the `figures-and-tables` folder.
To reproduce tables 8 and 9, you can simply execute the corresponding python script.
To reproduce tables 4,5,6,7 you should instead use the command-line utility `extract-single-channel-measurements.sh`. Read the `figures-and-tables/README.md' file for more instructions.

### To reproduce the benchmarks

Navigate to the `app-bench` folder and follow the instructions for building and executing benchmarks.

