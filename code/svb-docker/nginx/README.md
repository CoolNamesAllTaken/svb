## NGINX Reverse Proxy Configuration
[Useful tutorial](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Docker-Nginx-reverse-proxy-setup-example). Stuff is a little bit based off of this but also a lot of other sources, including Caitlin's work.

### Get Websites to Proxy Locally
1. Make each server entry in the .conf file listen to the relevant domain name.
2. Edit the hosts file (Windows: `C:\Windows\System32\drivers\etc\hosts` Linux: `/etc/hosts`) to add the relevant domain names.
```
# Added by John McNelly
127.0.0.1 johnmcnelly.com
127.0.0.1 www.johnmcnelly.com
127.0.0.1 pantsforbirds.com
127.0.0.1 www.pantsforbirds.com
# End of section
```

### Troubleshooting
#### Infinite redirect loop?
See [this article](https://wordpress.org/documentation/article/administration-over-ssl/#using-a-reverse-proxy) about changing wp-config.php. Probably not helpful since the docker container wordpress is already configured for reverse proxy stuff.

Run a command on the database to change the site URL to http://site_url instead of https://site_url if that was an issue.
```sql
UPDATE wp_options SET option_value = replace(option_value, 'https://pantsforbirds.com', 'http://pantsforbirds.com') WHERE option_name = 'home' OR option_name = 'siteurl';UPDATE wp_posts SET guid = replace(guid, 'https://pantsforbirds.com','http://pantsforbirds.com');UPDATE wp_posts SET post_content = replace(post_content, 'https://pantsforbirds.com', 'http://pantsforbirds.com'); UPDATE wp_postmeta SET meta_value = replace(meta_value,'https://pantsforbirds.com','http://pantsforbirds.com');
```

## Install Certbot
[Good Docker certbot tutorial](https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71). Most of the NGINX configuration is based off of this tutorial, with `init-letsencrypt.sh` being modified to support testing with local certificates.

Follow [this tutorial](https://www.pico.net/kb/how-do-you-get-chrome-to-accept-a-self-signed-certificate/) to add janky dummy certificates to Chrome for local testing over https.