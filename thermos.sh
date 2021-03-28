#!/usr/bin/bash

function write_temp() {

  for x in $(ls  /sys/bus/w1/devices/ | grep 28); do 
    echo "$x ""$(cat /sys/bus/w1/devices/w1_bus_master1/${x}/temperature)"; 
  done | python3 /home/r2h2/thermos.py >> /home/r2h2/logs/thermos/$fn

}


while true; do
  fn=$(date --iso-8601=minutes)
  write_temp
  sleep 300
done
