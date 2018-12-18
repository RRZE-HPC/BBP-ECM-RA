shopt -s extglob
# from https://stackoverflow.com/questions/20368577/bash-wildcard-n-digits

for size in 12500 125000 1250000 5000000 50000000 100000000 250000000
do
    grep -rH "Memory data volume" 18streams/bench.sz${size}.nrep+([0-9]).output.txt
    grep -rH "UNHALTED_CORE" 18streams/bench.sz${size}.nrep+([0-9]).output.txt
done

python parse_raw_data.py
