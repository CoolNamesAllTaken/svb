#!/bin/bash

# Usage: bash scripts/backup_scp_to_machine backups/johnmcnelly_backup_2023-08-20_22h22m55s.tar.gz
# Command above would put the backup in bird@birdbox.local:/home/bird/git-checkouts/birdbox/birdbox-docker/backups/johnmcnelly_backup_2023-08-20_22h22m55s.tar.gz.

backup_filename=$1
backup_name=$(basename $backup_filename)
local_backups_dir=$(dirname $backup_filename)
remote_backups_dir=/home/bird/git-checkouts/birdbox/birdbox-docker/backups
source $(dirname "$0")/../.env.birdbox

scp $local_backups_dir/$backup_name $MACHINE_SSH_USER@$MACHINE_SSH_HOST:$remote_backups_dir/$backup_name
