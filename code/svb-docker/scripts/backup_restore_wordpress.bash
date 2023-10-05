#!/bin/bash

####################################################################################################
# backup_restore_wordpress
# 
# This script restores a wordpress instance to a backed up version of its static files and database.
#
# Args:
#   website_name    Name of the website used as a base for container names, etc.
#   backup_name     Directory where the backup is stored. Static files should be in backup_dir/html,
#                   and database should be in backup_dir/APP-DATA.SQL.
#
# Example Usage:
#   bash scripts/backup_restore_wordpress.bash johnmcnelly backups/johnmcnelly_backup_2023-08-13_18h24m34s
#
# NOTE: This script requires the volumes being restored to be mounted to a vontainer. Containers do
# not need to be running for the restore to run successfully.
####################################################################################################

# Text Colors
color_red='\033[0;31m'
color_nc='\033[0m' # No Color

echo "Restoring Wordpress website from backup..."
website_name=$1 # first positional argument is website name, e.g. johnmcnelly
backup_name=$2
echo "backup_dir=$backup_name"
if [ $website_name == "" ]; then
    echo -e "\t${color_red}Missing required argument, please provide website name.${color_nc}"
    exit
elif [ ! -e $backup_name ]; then
    echo -e "\t${color_red}Backup directory or file $(pwd)/$backup_name does not exist, please provide a valid backup.${color_nc}"
    exit
fi
echo -e "\tWebsite Name: $website_name"
echo -e "\tBackup Directory or File: $backup_name"

docker_prefix=birdbox-docker

## Un-archive the backup if it's a .tar.gz file.
if [[ $backup_name == *.tar.gz ]]; then
    echo -e "\tDetected that backup directory is an archive, expanding..."
    backup_dir=${backup_name%%.*} # strip off file extension for backup directory name
    if [ -d $backup_dir ]; then
        echo -e "\t\t${color_red}Provided an archive backup, but a folder already exists with the same name.${color_nc}"
        exit
    fi
    mkdir $backup_dir # make the directory if it doesn't exist
    tar -xvf $backup_name -C $backup_dir
    echo -e "\t\tDone!"
    untarred_backup=true
else
    backup_dir=$backup_name
    untarred_backup=false
fi

## Upload Wordpress Content
site_container_name=$(docker ps -a --filter name=".*$website_name-wordpress-site.*" --format "{{.Names}}")
echo -e "\tRestoring wordpress content to $site_container_name..."

# Start the site container if it's not running yet.
if [ $(docker inspect -f '{{.State.Running}}' "$site_container_name") == "true" ]; then
    echo -e "\t\t$site_container_name is already running."
    site_container_already_started=true
else
    echo -e -n "\t\tStarting $site_container_name..."
    docker start $site_container_name > /dev/null
    sleep 5 # let site files get settled (some may be created on startup)
    echo -e "Done."
    site_container_already_started=false
fi

# Remove existing website files.
# Docker defaults to running in /var/www/html.
# Need to pass in "rm -r *" as a string so it doesn't expand to pattern in current directory outside container.
echo -e -n "\t\tDeleting old static files..."
docker exec $site_container_name sh -c "rm -r *" # clear out old static files
echo -e "Done!"

# Blast in the backed up website files.
echo -e -n "\t\tRestoring static files from backup..."
docker cp $backup_dir/html/. $site_container_name:/var/www/html # upload backed up static files
echo -e "Done!"

# Update file permissions to give ownership to www-data.
echo -e -n "\t\tUpdating file permissions to give ownership of /var/www/html to www-data:www-data..."
docker exec $site_container_name sh -c "chown -R www-data:www-data /var/www/html"
echo -e "Done!"

# Stop the site container if we started it just for the restore.
if [ $site_container_already_started == "false" ]; then
    # Database container was previously stopped, leave it stopped.
    echo -e -n "\t\tStopping $site_container_name..."
    docker stop $site_container_name > /dev/null
    echo -e "Done."
fi

## Upload Database Content
db_container_name=$(docker ps -a --filter name=".*$website_name-wordpress-db.*" --format "{{.Names}}")
db_env_file=$(dirname "$0")/../wordpress/.env.$website_name
source $db_env_file # load database credentials
echo -e "\tLoaded database credentials from $db_env_file."
echo -e "\tRestoring database content to $db_container_name..."

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

# Restore the database from the backup.
echo -e "\t\tRestoring database from backup..."
mysql_dump=$backup_dir/APP-DATA.SQL
# For some reason I can't restore directly into the docker container from a local file, I need to copy it into the container first...
docker cp $mysql_dump $db_container_name:/tmp/APP-DATA.SQL
docker exec $db_container_name sh -c "mysql --user=root --password=$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE < /tmp/APP-DATA.SQL"
# TODO: The line below doesn't work? Maybe something with relative paths.
# docker exec $db_container_name mysql --user=root --password=$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE < $mysql_dump
echo -e "\t\t\tImported database $MYSQL_DATABASE from MySQL dump file $mysql_dump"
echo -e "\t\t\tDone!"

# Stop the database container if we started it just for the backup.
if [ $db_container_already_started == "false" ]; then
    # Database container was previously stopped, leave it stopped.
    echo -e -n "\t\tStopping $db_container_name..."
    docker stop $db_container_name > /dev/null
    echo -e "Done."
fi

echo -e "\t\tDatabase restore complete."

## Remove backup folder if one was created.
if [ $untarred_backup == "true" ]; then
    echo -e -n "\tCleaning up backup directory $backup_dir..."
    rm -rf $backup_dir
    echo -e "Done!"
fi

echo -e "\tWordpress website restore complete."
