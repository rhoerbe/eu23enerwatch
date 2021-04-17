#!/usr/bin/env bash

# delete directories 2 months back

logdirroot='/home/r2h2/logs/thermos'

# keep at least 3 month of data
purgemonth=$(date --date 'now - 4 month' '+%Y-%m')

rm -rf $logdirroot/${purgemonth}-*
