#!/bin/bash

source $(dirname "$0")/../.env.birdbox
scripts_dir=$(dirname "$0")
backups_dir=$(dirname "$0")/../backups

for website_name in "${WEBSITE_NAMES[@]}"; do
    bash $scripts_dir/backup_download_wordpress.bash $website_name
done

rsync -avx --delete $backups_dir $STORAGE_SSH_USER@$STORAGE_SSH_HOST:$STORAGE_BACKUP_DIR