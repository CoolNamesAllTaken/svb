#!/bin/bash

# Usage: bash systemd/install_dns_update_service.bash /etc/systemd/system

update_dns_script_filename=$(realpath $(dirname "$0")/../scripts/dns_update_godaddy_records.bash)

services_dir=$1
service_name=birdbox-dns
service_filename=$services_dir/$service_name.service
timer_filename=$services_dir/$service_name.timer

# Text Colors
color_red='\033[0;31m'
color_nc='\033[0m' # No Color

if [ ! -d $services_dir ]; then
    echo -e "${color_red}Services directory $services_dir is not a valid directory.${color_nc}"
    exit
fi

cat > $services_dir/$service_name.service << endmsg

[Unit]
Description=DNS record update service for birdbox.

[Service]
ExecStart=/bin/bash -c "$update_dns_script_filename"

[Install]
WantedBy=multi-user.target

endmsg

if [ ! -e $service_filename ]; then
    echo -e "${color_red}Failed to create service file $service_filename. Try with sudo?${color_nc}"
    exit
else
    echo -e "Service file created at $service_filename."
fi

cat > $services_dir/$service_name.timer << endmsg

[Unit]
Description=Timer for regularly triggering birdbox DNS updates.

[Timer]
Unit=$service_name.service
# Update DNS record every 15 minutes.
OnCalendar=*:0,15,30,45
Persistent=True

[Install]
WantedBy=multi-user.target

endmsg

if [ ! -e $timer_filename ]; then
    echo -e "${color_red}Failed to create timer file $timer_filename. Try with sudo?${color_nc}"
    exit
else
    echo -e "Service file created at $timer_filename."
fi

chmod +x $update_dns_script_filename
echo "Made $update_dns_script_filename executable."