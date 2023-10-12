# Docker Commands
Note: These commands must be run from the `svb-docker` directory.

Mac / Linux: You should be fine.

Windows: Install Git Bash.

## Installation on a new development machine for localhost testing
1. Install Docker Desktop.
2. Run `docker compose up --build`. Run with the `-d` option if you want it to be detached (non-interactive).

## Bring Stuff Up
`docker compose up --build`

### Just add/modify a model?
Run migrations!
`docker compose -f compose.yml exec site python manage.py makemigrations`
Then `docker compose -f compose.yml exec site python manage.py migrate`

## Where is everything?
1. Container configuration info: `docker-compose.yaml`.
2. Credentials: `env.svb` (DO NOT COMMIT THIS FILE). Sample credentials: `env.svb.sample`.
    * Base URLs that A records should be updated for, SSL certificate URLs: DOMAINS.
    * Database credentials for PostgreSQL database.
3. Reverse proxy settings: `nginx/app.conf`.