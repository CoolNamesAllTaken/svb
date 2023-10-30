# SVB Django

# What are all these directories?
Note: this README resides in `svb_web`, the top level Django project folder. The following folders and files are
subdirectories within the top level `svb_web` folder.

* `core` - The main Django app.
    * `migrations` - Don't touch this. 
    * `static` - Static files to be served by Django.
        * `core`
            * `assets` - All widely reused website images go in here (logos, favicon, etc).
            * `css` - Stylesheets. Contins the baseline bootstrap stylesheet (so we can operate offline) and some overrides in `styles.css`.
    * `templates` - HTML templates that can be "hydrated" by contexts provided by functions in `views.py`.
    * `admin.py` - 
    * `models.py` - Database models used by the Django app.
    * `tests.py` - Hahahahaha.
    * `urls.py` - URL tree for the website. Specifies a render function and HTML template for each URL, and calls the corresponding render
        function in `views.py` when that page is requested.
    * `views.py` - Rendering functions for each of the pages. Function names should match names in `urls.py` and return a context that can be
        used to rehydrate the template HTML served by `urls.py`.
* `svb_web` - Default folder for the SVB project. Contains important top-level stuff for the project.
    * `asgi.py` - Lol idk.
    * `urls.py` - Top level URL tree for the whole website. Has the admin interface then redirects everything
        else to the `core` app's URL tree.
    * `settings.py` - Settings for the Django project. Reads all of its secret stuff from `../../.env.svb` file.
    * `wsgi.py` - Lol idk.


# Running manage.py Commands
Run these commands from the same directory as compose.yml.

Enter the docker container running the Django app: `docker compose exec site bash`.

Useful commands once you're there:
```bash
python manage.py createsuperuser # Don't use this, we've already run it.
python manage.py makemigrations # Run this before migrations.
python manage.py migrate # Migrates databases with new models etc.
```

## Creating New Models
1. Create the model in `models.py`.
2. Import the model into relevant other places.
3. Register the model in `admin.py` to allow messing around with them in the django admin page.
4. Run `makemigations` and `migrate` with `manage.py`.

## References
* [Tutorial: Setting up Django with PostgreSQL database](https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8)
* [Tutorial: Django with Docker Compose](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
* [Tutorial: Python Dotenv Examples](https://dev.to/emma_donery/python-dotenv-keep-your-secrets-safe-4ocn)

## Online Tools
* [Favicon Generator](https://realfavicongenerator.net/)