#!/usr/bin/env bash

# 1. Sync transfer directory (rclone/eu23automation/xfer) to mirror the server side
# 2. Check sameness and report error unless OK
# 3. Move new log files to transfer directory
# 4. Copy local directory to server
# (Files will be archived on the server side after processing, next sync will delete them locally)

localdir='onedrive:eu23automation/'
remotedir='/home/r2h2/rclone/eu23automation/'
logdir='/var/log/rclone'


rclone sync -v $localdir $remotedir > $logdir/move2cloud.log 2>&1
now=$( date --iso-8601=seconds)
if rclone check -v $localdir $remotedir >> $logdir/move2cloud.log 2>&1; then
  mv logs/thermos/ &localdir
  rclone copy -v $localdir $remotedir >> $logdir/move2cloud.log 2>&1
else
  echo "Subject: $HOSTNAME: rclone check with OneDrive failed at $now" | sendmail rainer@hoerbe.at
  # system unit nullmailer does not work -> needs manual kick
  /usr/sbin/nullmailer-send &
  sleep 10
  kill %1
  exit 1
fi
