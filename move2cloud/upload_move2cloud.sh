#!/usr/bin/env bash

# 1. Sync transfer directory (rclone/eu23automation/xfer) to mirror the server side
# 2. Check sameness and report error unless OK
# 3. Move new log files to staging directory
# 4. Upload staging directory to cloud server
# (Files will be archived on the server side after processing, next sync will delete them locally)

sourcedir='/home/r2h2/logs/thermos'
stagingdir='/home/r2h2/logstaging'
archivedir='/home/r2h2/logarchive'
localdir='onedrive:eu23automation'
remotedir='/home/r2h2/rclone/eu23automation'
logdir='/var/log/rclone'
start=$( date --iso-8601=seconds)


main () {
  s1_sync_cloud || echo "$start rclone sync failed." >> $logdir/move2cloud.log; finalize
  s2_sync_check || echo "$start rclone check failed." >> $logdir/move2cloud.log; finalize
  s3_move_log_to_staging
  s4_upload_to_database
  s5_upload_staging_to_cloud || echo "$start rclone copy failed." >> $logdir/move2cloud.log; finalize
  s6_move_staging_to_archive  # to be collected by logrotate
}

s1_sync_cloud() {
  rclone sync -v $localdir/ $remotedir/ > $logdir/move2cloud.log 2>&1
  return $?
}


s2_check_cloud() {
  rclone check -v $localdir/ $remotedir/ > $logdir/move2cloud.log 2>&1
  return $?
}


s3_move_log_to_staging() {
  mkdir -p $stagingdir
  mv $sourcedir/* $stagingdir/
}


function s4_upload_to_database() {
  ../upload2db/upload2db.sh
}


s5_upload_staging_to_cloud() {
  rclone copy -v $localdir/ $remotedir/ >> $logdir/move2cloud.log 2>&1
  return $?
}


s6_move_staging_to_archive() {
  mkdir -p $archivedir
  mv $stagingdir/* $archivedir/
}


finalize() {
  echo "Subject: $HOSTNAME: move2cloud.sh started at $now failed" | sendmail rainer@hoerbe.at
  # system unit nullmailer does not work -> needs manual kick
  /usr/sbin/nullmailer-send &
  sleep 10
  kill %1
  exit 1
}


main $@
