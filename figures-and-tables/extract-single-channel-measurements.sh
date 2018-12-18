# if output is off by a factor 10, 100 or 1000
# see [WARNING] below

echo "Usage: ./extract-single-channel-measurements.sh <CHANNELNAME> <CACHELEVEL>"
CHANNELNAME=$1
CACHELEVEL=$2

echo "[W] Output could be off by a factor 10, 100 or 1000"
echo "See [WARNING] inside file for more information"

BASE_RESULTS_PATH=../results/single-channel-bench

for ARCH in ivb tds 
do
    case $CHANNELNAME in
    Ih)
        KERNELNAME=state
        if [ "${CACHELEVEL}" == "L2" ]
        then
            if [ "${ARCH}" == "tds" ]
            then
                NINSTANCES=5412
            else
                NINSTANCES=1353
            fi
        else
            NINSTANCES=55350
        fi
    ;;
    ##############################################
    Im)
        KERNELNAME=current
        if [ "${CACHELEVEL}" == "L2" ]
        then
            if [ "${ARCH}" == "tds" ]
            then
                NINSTANCES=1476
            else
                NINSTANCES=369
            fi
        else
            NINSTANCES=49323
        fi
    ;;
    ##############################################
    # NINSTANCES for AMPA is the same for state and current
    DetAMPANMDA)
        echo "To switch between current and state"
        echo "uncomment relevant section within file"
        echo "around line 50"
        #KERNELNAME=current
        KERNELNAME=state
        if [ "${CACHELEVEL}" == "L2" ]
        then
            if [ "${ARCH}" == "tds" ]
            then
                NINSTANCES=2400
            else
                NINSTANCES=4000
            fi
        else
            if [ "${ARCH}" == "tds" ]
            then
                NINSTANCES=56000
            else
                NINSTANCES=7000
            fi
        fi
    ;;
    esac

    if [ "${ARCH}" == "tds" ]
    then
        NTREP=200
    else
        NTREP=20
    fi

    # [WARNING] NSTATSREP corresponds to the number
    # of repetitions in a row of the kernel that were made
    # purely for benchmarking purposes.
    # Since this value was somewhat tailored for different
    # configurations to avoid very very long benchmarks
    # some outputs could be wrong!
    # In any case, I always used multiples of 10 for NSTATSREP.
    # Please adjust below accordingly

    if [ "${KERNELNAME}" == 'state' ]
    then
        NSTATSREP=100 # or maybe 10, 1000, 10000
    else
        NSTATSREP=1000 # or maybe 10000
    fi

    echo "########## $ARCH ##############"
    echo "---- $CHANNELNAME $KERNELNAME ---- "
    # small hacks:
    if [ "${CHANNELNAME}" == "DetAMPANMDA" ]
    then
        KERNELNAME=EMS_${KERNELNAME}
    fi
    if [ "${ARCH}" == "tds" ]
    then
        TOADD="1cells_"
    else
        TOADD=""
    fi

    ########################
    # HERE WE GET THE ACTUAL NUMBERS
    for VECT in SSE AVX AVX512
    do
        echo "----- $VECT $CACHELEVEL ------"
        grep -nrH -A 7 "${CHANNELNAME}_${KERNELNAME},Group 1 Raw" ${BASE_RESULTS_PATH}/bench_ECM_theoretical_L5_TTPC1_${CHANNELNAME}_${TOADD}${VECT}_${ARCH}_${CACHELEVEL}/  | grep CPU_CLK_UNHALTED_CORE | awk -F',' -v ntrep=${NTREP} -v nstatsrep=${NSTATSREP} -v ninstances=${NINSTANCES} '{print $3/(ntrep*nstatsrep*ninstances)}' | sort -n
    done
done
