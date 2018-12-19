### To reproduce a figure or table

simply execute the python script with the corresponding name.
N.B. must use python 3

### To reproduce tables 4,6

Use the `extract-single-channel-measurements.sh` script.
Usage:

```
$ ./extract-single-channel-measurements.sh <NAME OF CHANNEL> <CACHE LEVEL>
```

For example

```
$ ./extract-single-channel-measurements.sh Ih L2
```

##### Important warning

For simplicity, I sometimes changed the number of repetitions of a given kernel.
This means that the output of the `extract-single-channel-measurements.sh` script might be off by exactly a factor 10, 100 or even 1000 compared to the tables.
I never used number of repetitions that were not multiples of 10.

### To reproduce tables 5,7

Comment out the `current` or `state` line in the `extract-single-channel-measurements.sh` within the DetAMPANMDA case block, around line 51, according to the kernel of your interest, then

```
$ ./extract-single-channel-measurements.sh DetAMPANMDA L2
```

##### Important warning

For simplicity, I sometimes changed the number of repetitions of a given kernel.
This means that the output of the `extract-single-channel-measurements.sh` script might be off by exactly a factor 10, 100 or even 1000 compared to the tables.
I never used number of repetitions that were not multiples of 10.

