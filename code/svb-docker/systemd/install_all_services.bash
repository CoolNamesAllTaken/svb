source $(dirname "$0")/../.env.birdbox

bash $(dirname "$0")/install_docker_compose_service.bash $SYSTEMD_SERVICES_DIR
systemctl enable birdbox-docker
systemctl start birdbox-docker

bash $(dirname "$0")/install_dns_update_service.bash $SYSTEMD_SERVICES_DIR
systemctl enable birdbox-dns
systemctl daemon-reload # reload the systemd daemon to load the new that was created
systemctl start birdbox-dns.timer