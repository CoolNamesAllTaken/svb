#!/bin/bash

# Usage: bash scripts/mysql_show_tables.sh johnmcnelly

website_name=$1

db_container_name=$(docker ps -a --filter name=".*$website_name-wordpress-db.*" --format "{{.Names}}")
db_env_file=$(dirname "$0")/../wordpress/.env.$website_name
source $db_env_file # load database credentials

docker exec $db_container_name mysql --user=root --password=$MYSQL_ROOT_PASSWORD -e "USE $MYSQL_DATABASE; SHOW TABLES;"