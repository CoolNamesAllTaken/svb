#!/bin/bash

# Load variables.
source $(dirname "$0")/../.env.birdbox
data_path=$(dirname "$0")/../certbot/data # Set this to the certbot folder to dump all the generated stuff into.
docker_compose_path=$(dirname "$0")/../docker-compose.yml

if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

for domain in "${DOMAINS[@]}"; do
  domain_folder_path=$data_path/conf/live/$domain

  if [ -d "$domain_folder_path" ]; then
    read -p "Existing data found for $domain. Continue and replace existing certificate? (y/N) " decision
    if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
      continue
    else
      rm -rf $domain_folder_path
    fi
  fi

  echo "### Creating dummy certificate for $domain ..."
  domain_path="/etc/letsencrypt/live/$domain"
  mkdir -p "$data_path/conf/live/$domain"
  docker compose -f $docker_compose_path run --rm --entrypoint "\
    openssl req -x509 -nodes -newkey rsa:$SSL_RSA_KEY_SIZE -days 1\
      -keyout '$domain_path/privkey.pem' \
      -out '$domain_path/fullchain.pem' \
      -subj '/C=$SSL_CERT_COUNTRY/ST=$SSL_CERT_STATE/L=$SSL_CERT_CITY/O=$SSL_CERT_ORGANIZATION/OU=$SSL_CERT_ORGANIZATIONAL_UNIT/CN=$domain'" certbot
  echo

  if [ $SSL_DUMMY_CERTS_ONLY != "0" ]; then
    echo "Exiting now to keep dummy certs for localhost testing."
    continue # bail out before deleting dummy certs, so they can be used for localhost testing
  else
    echo "No localhost testing this time..."
  fi

  echo "### Starting nginx ..."
  docker compose -f $docker_compose_path up --force-recreate -d nginx
  echo

  echo "### Deleting dummy certificate for $domain ..."
  docker compose -f $docker_compose_path run --rm --entrypoint "\
    rm -Rf /etc/letsencrypt/live/$domain && \
    rm -Rf /etc/letsencrypt/archive/$domain && \
    rm -Rf /etc/letsencrypt/renewal/$domain.conf" certbot
  echo

  # 2023-08-20 commented out the section below, since it's for multiple URLs with the same certificate. We want
  # multiple URLs, each with a different certificate.
  # echo "### Requesting Let's Encrypt certificate for $DOMAINS ..."
  # # Join $DOMAINS to -d args
  # domain_args=""
  # for domain in "${DOMAINS[@]}"; do
  #   domain_args="$domain_args -d $domain"
  domain_args=" -d $domain"


  # Select appropriate email arg
  case "$SSL_EMAIL" in
    "") email_arg="--register-unsafely-without-email" ;;
    *) email_arg="--email $SSL_EMAIL" ;;
  esac

  # Enable staging mode if needed
  if [ $SSL_STAGING != "0" ]; then staging_arg="--staging"; fi

  docker compose -f $docker_compose_path run --rm --entrypoint "\
    certbot certonly --webroot -w /var/www/certbot \
      $staging_arg \
      $email_arg \
      $domain_args \
      --rsa-key-size $SSL_RSA_KEY_SIZE \
      --agree-tos \
      --force-renewal" certbot
done

echo "### Reloading nginx ..."
docker compose -f $docker_compose_path exec nginx nginx -s reload
