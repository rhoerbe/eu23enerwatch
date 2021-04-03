#!/usr/bin/bash

logdirroot='/home/r2h2/logs/thermos'
lastlogfp='/var/log/sample_temp/lastlog'
sampling_interval=300


function main() {
  while true; do
    local todaydir=$(date --iso-8601)
    mkdir -p $logdirroot/$todaydir
    local fn=$(date --iso-8601=minutes)
    fp=$logdirroot/$todaydir/$fn
    write_temp
    rm $logdirroot/*    # remove empty regular files -> not found where created
    sleep $sampling_interval
  done
}


function write_temp() {

  for x in $(ls  /sys/bus/w1/devices/ | grep 28); do 
    echo "$x ""$(cat /sys/bus/w1/devices/w1_bus_master1/${x}/temperature)"  >> $fp
  done
  printf "$fp created with " > $lastlogfp
  stat --printf="%s" $fp  >> $lastlogfp
  printf " bytes\n" >> $lastlogfp
}


main $@
