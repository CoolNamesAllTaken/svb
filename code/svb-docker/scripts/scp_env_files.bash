source $(dirname "$0")/../.env.birdbox

birdbox_dir=$(dirname "$0")/..
wordpress_dir=$(dirname "$0")/../wordpress

# Copy wordpress .env files for each website.
for website_name in "${WEBSITE_NAMES[@]}"; do
    local_env_filename=$wordpress_dir/.env.$website_name
    remote_env_filename=$MACHINE_SSH_USER@$MACHINE_SSH_HOST:$MACHINE_BIRDBOX_DIR/birdbox-docker/wordpress/.env.$website_name
    echo "Copying wordpress .env file for $website_name from $local_env_filename to $remote_env_filename"
    scp $local_env_filename $remote_env_filename
done

# Copy master .env file for everything.
local_env_filename=$birdbox_dir/.env.birdbox
remote_env_filename=$MACHINE_SSH_USER@$MACHINE_SSH_HOST:$MACHINE_BIRDBOX_DIR/birdbox-docker/.env.birdbox
echo "Copying master .env.birdbox file from $local_env_filename to $remote_env_filename"
scp $local_env_filename $remote_env_filename