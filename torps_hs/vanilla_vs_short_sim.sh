#! /bin/bash

BASE_DIR=/vol/tmp/wedel/torps
#BASE_DIR=$HOME/Studium/Diplomarbeit/Data/torps

DATE_RANGE='2014-02--2014-12'
OUTPUT="relay-adv"
NUM_PROCESSES=10
ADV_TIME=0
NUM_ADV_GUARDS=1
NUM_ADV_MIDDLES=1
NUM_ADV_EXITS=0
ADV_EXIT_BW=0
USERMODEL=hs_only_simple=1200 # 20min 3600(1hour)
NUM_SAMPLES=5000
LOGLEVEL="INFO"
# PATH_ALG=hs_torg

# guard_r_squared = 0.698512970655
guard_a=297.655588881
guard_b=1717416.85555
# middles_r_squared = 0.73438857015
middle_a=316.432097094
middle_b=882989.126045

# FULL_BW=104857600 #(100MiB)
# FULL_BW=209715200 #(200MiB)
FULL_BW=419430400 #400MiB
# FULL_BW=838860800 #800MiB
FULLBW_STR='400MiB'

RATIOS=('1:0') #('50:1') # '9:1' '1:0')
DIVS=(1) # 0.9 1 0.98)

DIRTO= 'final_vanilla_vs_short_honeypot'
NUM_ADV='1adv'

NSF_DIR=$BASE_DIR/out/network-state/ns-$DATE_RANGE
echo "Hello. Will simulate with $FULLBW_STR FullBW."

pids=""
for PATH_ALG in 'hs_tor_honeypot' 'hs_short_tor_honeypot' #'hs_tor' 'hs_short_tor'
do

  echo "Will simulate for $PATH_ALG ($FULLBW_STR)."

  SIM_OUT_DIR=$BASE_DIR/out/simulate/$DIRTO/$FULLBW_STR/$PATH_ALG-$NUM_ADV
  ANA_OUT_DIR=$BASE_DIR/out/analyze/$DIRTO/$FULLBW_STR/$PATH_ALG-$NUM_ADV

  mkdir -p $BASE_DIR/out/simulate/$DIRTO
  mkdir -p $BASE_DIR/out/analyze/$DIRTO
  mkdir -p $BASE_DIR/out/simulate/$DIRTO/$FULLBW_STR/
  mkdir -p $BASE_DIR/out/analyze/$DIRTO/$FULLBW_STR/
  mkdir -p $SIM_OUT_DIR
  mkdir -p $ANA_OUT_DIR

  i=0
  while [[ $i -lt ${#RATIOS[@]} ]]
  do
    # echo $i ${DIVS[i]} ${RATIOS[i]}
    ADV_GUARD_BW=`echo "scale=0; ($FULL_BW*${DIVS[i]})/$NUM_ADV_GUARDS"|bc`
    ADV_MIDDLE_BW=`echo "scale=0; ($FULL_BW*(1-${DIVS[i]}))/$NUM_ADV_MIDDLES" |bc -l`
    ADV_GUARD_CONS=`echo "scale=0; ($ADV_GUARD_BW-$guard_b)/$guard_a" |bc -l`
    ADV_MIDDLE_CONS=`echo "scale=0; ($ADV_MIDDLE_BW-$middle_b)/$middle_a" |bc -l`
    RATIO=${RATIOS[i]}
    EXP_NAME=$ADV_GUARD_BW-$ADV_MIDDLE_BW-$NUM_ADV
    mkdir -p $SIM_OUT_DIR/$RATIO
    # ADV_FULL_BW=`echo "scale=0; $ADV_GUARD_BW+$ADV_MIDDLE_BW/1" |bc -l`
    if [ $ADV_GUARD_CONS -lt 0 ]
      then
        ADV_GUARD_CONS=0
      fi
    if [ $ADV_MIDDLE_CONS -lt 0 ]
      then
        ADV_MIDDLE_CONS=0
      fi

    echo "Will start simulating with Ratio $RATIO ($EXP_NAME) [$FULLBW_STR]."
    echo "Guard: $ADV_GUARD_BW Byte = $ADV_GUARD_CONS Cons"
    echo "Middle: $ADV_MIDDLE_BW Byte = $ADV_MIDDLE_CONS Cons"
    # echo "python pathsim.py simulate --nsf_dir $NSF_DIR\
    #  --num_samples $NUM_SAMPLES --user_model $USERMODEL\
    #  --format $OUTPUT --adv_guard_cons_bw $ADV_GUARD_CONS\
    #  --adv_exit_cons_bw $ADV_EXIT_BW --adv_time $ADV_TIME\
    #  --num_adv_guards $NUM_ADV_GUARDS --num_adv_exits $NUM_ADV_EXITS\
    #  --num_adv_middles $NUM_ADV_MIDDLES --adv_middle_cons_bw $ADV_MIDDLE_CONS\
    #  --loglevel $LOGLEVEL $PATH_ALG"
    num_proz=1
    while [[ $num_proz -le $NUM_PROCESSES ]]
    do
      (time python pathsim.py simulate --nsf_dir $NSF_DIR\
       --num_samples $NUM_SAMPLES --user_model $USERMODEL\
       --format $OUTPUT --adv_guard_cons_bw $ADV_GUARD_CONS\
       --adv_exit_cons_bw $ADV_EXIT_BW --adv_time $ADV_TIME\
       --num_adv_guards $NUM_ADV_GUARDS --num_adv_exits $NUM_ADV_EXITS\
       --num_adv_middles $NUM_ADV_MIDDLES --adv_middle_cons_bw $ADV_MIDDLE_CONS\
       --loglevel $LOGLEVEL $PATH_ALG)\
       2> $SIM_OUT_DIR/$RATIO/simulate.$EXP_NAME.$NUM_SAMPLES-samples.$num_proz.time\
       1> $SIM_OUT_DIR/$RATIO/simulate.$EXP_NAME.$NUM_SAMPLES-samples.$num_proz.out &
      pids="$pids $!"
      mkdir -p $SIM_OUT_DIR/$RATIO/logs
      mkdir -p $SIM_OUT_DIR/$RATIO/time
      num_proz=$(($num_proz+1))
    done
    i=$(($i+1))
  done
done
for pid in $pids
do
    wait $pid
done

echo 'Done simulating. Will now analyze...'


pids=""
for PATH_ALG in 'hs_tor_honeypot' 'hs_short_tor_honeypot' #'hs_tor' 'hs_short_tor'
do
  echo "Will analyze for $PATH_ALG"
  SIM_OUT_DIR=$BASE_DIR/out/simulate/$DIRTO/$FULLBW_STR/$PATH_ALG-$NUM_ADV
  ANA_OUT_DIR=$BASE_DIR/out/analyze/$DIRTO/$FULLBW_STR/$PATH_ALG-$NUM_ADV
  i=0
  while [[ $i -lt ${#RATIOS[@]} ]]
  do
    # echo $i ${DIVS[i]} ${RATIOS[i]}
    ADV_GUARD_BW=`echo "scale=0; ($FULL_BW*${DIVS[i]})/$NUM_ADV_GUARDS"|bc`
    ADV_MIDDLE_BW=`echo "scale=0; ($FULL_BW*(1-${DIVS[i]}))/$NUM_ADV_MIDDLES" |bc -l`
    RATIO=${RATIOS[i]}
    EXP_NAME=$ADV_GUARD_BW-$ADV_MIDDLE_BW-adv

    mv $SIM_OUT_DIR/$RATIO/*.out $SIM_OUT_DIR/$RATIO/logs 2> /dev/null
    mv $SIM_OUT_DIR/$RATIO/*.time $SIM_OUT_DIR/$RATIO/time 2> /dev/null

    mkdir -p $ANA_OUT_DIR/$RATIO

    LOGS_IN=$SIM_OUT_DIR/$RATIO/logs
    DATA_OUT=$ANA_OUT_DIR/$RATIO

    echo "Will start analyzing with Ratio $RATIO [$FULLBW_STR]"
    python hs_pathsim_analysis_new.py simulation-set $LOGS_IN $DATA_OUT $EXP_NAME &
    pids="$pids $!"

    i=$(($i+1))
  done
done
for pid in $pids
do
    wait $pid
done

echo 'Done. Goodby.'
