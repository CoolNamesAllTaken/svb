#!/bin/bash

####################################################################################################
# backup_download_wordpress
# 
# This script downloads a backup of the specified wordpress website, including static files and
# database contents.
#
# Args:
# website_name Name of the website, used as a base for container names etc.
#
# Example Usage:
#   backup_download_wordpress johnmcnelly
#
# NOTE: This script requires the volumes being backed up to be mounted to a vontainer. Containers
# do not need to be running for the backup to run successfully.
####################################################################################################

echo "Creating Wordpress website backup..."
website_name=$1 # first positional argument is website name, e.g. johnmcnelly
if [ -e $website_name ]; then
    echo -e "\tMissing required argument, please provide website name."
    exit
else
    echo -e "\tWebsite Name: $website_name"
fi

docker_prefix=birdbox-docker
# SED_NEWLINE_REPLACEMENT_STRING=':a;N;$!ba;s/\n/                                                                                \r/g'

backups_dir=$(dirname "$0")/../backups
backup_name=$website_name"_backup_$(date +%Y-%m-%d_%H\h%M\m%S\s)"
backup_dir=$backups_dir"/"$backup_name
echo -e "\tBackup Directory: $backup_dir."
mkdir $backup_dir

## Download Wordpress Content
site_container_name=$(docker ps -a --filter name=".*$website_name-wordpress-site.*" --format "{{.Names}}")
echo -e -n "\tDownloading wordpress content from $site_container_name..."
docker cp $site_container_name:/var/www/html/ $backup_dir
echo -e "Done!"

## Download Database Content
db_container_name=$(docker ps -a --filter name=".*$website_name-wordpress-db.*" --format "{{.Names}}")
db_env_file=$(dirname "$0")/../wordpress/.env.$website_name
source $db_env_file # load database credentials
echo -e "\tLoaded database credentials from $db_env_file."
echo -e "\tDownloading database content from $db_container_name..."

# Start the database container if it's not running yet.
if [ $(docker inspect -f '{{.State.Running}}' "$db_container_name") == "true" ]; then
    echo -e "\t\t$db_container_name is already running."
    db_container_already_started=true
else
    echo -e -n "\t\tStarting $db_container_name..."
    docker start $db_container_name > /dev/null
    sleep 1 # let database get settled
    echo -e "Done."
    db_container_already_started=false
fi

# Dump the database.
docker exec $db_container_name mysqldump --user=root --password=$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE > $backup_dir/APP-DATA.SQL

# Stop the database container if we started it just for the backup.
if [ $db_container_already_started == "false" ]; then
    # Database container was previously stopped, leave it stopped.
    echo -e -n "\t\tStopping $db_container_name..."
    docker stop $db_container_name > /dev/null
    echo -e "Done."
fi

echo -e "\t\tDatabase download complete."

echo -e "\tCreating archive..."
# Archive all the website files without pre-pending the full path of the backups folder to each file's name.
# Note that the -C option is order-sensitive. https://www.gnu.org/software/tar/manual/html_node/directory.html#directory
tar -zcvf $backup_dir.tar.gz -C $backup_dir . #| sed "$SED_NEWLINE_REPLACEMENT_STRING"
echo -e "\t\tDone!"

echo -e -n "\tDeleting folder of crap..."
rm -rf $backup_dir
echo -e "Done!"

echo -e "\tWordpress website backup complete."
