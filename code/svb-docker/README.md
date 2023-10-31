# Docker Commands
Note: These commands must be run from the `svb-docker` directory.

Mac / Linux: You should be fine.

Windows: Install Git Bash.

## Installation on a new development machine for localhost testing
1. Install Docker Desktop.
2. Run `docker compose up --build`. Run with the `-d` option if you want it to be detached (non-interactive).
3. Use `docker compose exec site bash` to run `python manage.py createsuperuser` in the `site` docker container.
4. Go to `localhost:8000/internal` and login with the credentials created in step 3.
5. Go to the "Manager" tab and initialize the bank.

## Bring Stuff Up
Development: `docker compose up --build`
Production: `docker compose -f compose.prod.yml --build`

### Just add/modify a model?
Run migrations!
`docker compose -f compose.yml exec site python manage.py makemigrations`
Then `docker compose -f compose.yml exec site python manage.py migrate`
Be sure to commit your migrations with your code!

## Where is everything?
1. Container configuration info: `docker-compose.yaml`.
2. Credentials: `env.svb` (DO NOT COMMIT THIS FILE). Sample credentials: `env.svb.sample`.
    * Base URLs that A records should be updated for, SSL certificate URLs: DOMAINS.
    * Database credentials for PostgreSQL database.
3. Reverse proxy settings: `nginx/app.conf`.