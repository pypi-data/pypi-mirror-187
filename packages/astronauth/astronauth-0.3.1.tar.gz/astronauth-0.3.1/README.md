# ASTRONauth

Django App for quickly adding authentication to any Django app.

`astronauth` is based on the `allauth` package and updates the templates for follow the Design in ASTRON style (DIAS).

## Installation

The package is available on pypi:

```bash
pip install astronauth
```

### Django Settings

The following settings are the minimal settings required (also check the [settings.py](integration/integration/settings.py) file.):

- `SITE_ID` is used by `allauth`, usually it can be set to `1` without any issue. See the [Django documentation](https://docs.djangoproject.com/en/4.1/ref/contrib/sites/) for more info.
- `INSTALLED_APPS`: make sure `astronauth` is listed before `allauth` since it overrides templates
```python
INSTALLED_APPS = [
    # These are the default and should already be included
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "my_app",   # if you override any of the templates, this should be here (e.g. custom navigation bar)

    ## These are required for ASTRONauth
    'django.contrib.sites',
    "astronauth",   # it is important that astronauth is included before allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.keycloak',
]
```
- `SOCIALACCOUNT_PROVIDERS`: is a list of auth providers. `astronauth` mainly uses Keycloak:
```python
SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': 'https://sdc-dev.astron.nl/auth',   # replace by https://keycloak.astron.nl/auth/ for production
        'KEYCLOAK_REALM': 'SDC',    # change this depending on which realm to use
        'SCOPE': ['openid', 'profile', 'email']
    }
}
```

- `SOCIALACCOUNT_ADAPTER`: is the python class which populates the `User` and `UserProfile` models. Since we want to store location information, we need to specify our custom Adapter:
```python
SOCIALACCOUNT_ADAPTER = "astronauth.socialaccount.adapter.SocialAccountAdapter"
```

- `LOGIN_REDIRECT_URL` is used to determine where users should be redirected after login. Usually the main index page is a good one (`http://localhost:8000/` is used in development)

- While `DEBUG=True` Django hosts the file. For production purposes, consider the Django recommendations form their [documentation](https://docs.djangoproject.com/en/4.1/howto/static-files/deployment/).

- **Important**: with this configured, you should migrate the database: `python manage.py migrate` before further configuration. Also create a `superuser`:

```bash
$ DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --username admin --email no-reply@example.com --noinput
```

**Important**: replace the username/password and email where necessary


Since `astronauth` is based on `allauth`, please take a look at their [documentation](https://django-allauth.readthedocs.io/en/latest/installation.html) for all available settings.

#### Rename session and CSRF Cookies

If multiple apps or services are hosted at the same machine/url, their session or csrf cookies might interfere.
Therefore it is necessary to rename the session and csrf cookies to include the name of the app.
Add the following to your `settings.py` in your Django project folder:

```python
SESSION_COOKIE_NAME = 'my_service_name_session_id'
CSRF_COOKIE_NAME = 'my_service_csrftoken'
```

### Adding a provider

Before adding the provider in your app, make sure you have a [realm setup in Keycloak](https://www.keycloak.org/docs/13.0/getting_started/#creating-a-realm-and-a-user) and [configured a client](https://www.keycloak.org/docs/13.0/getting_started/#registering-the-wildfly-application) in that Keycloak realm. Take note of the `Client ID`, since you will use it in `astronauth`.

Make sure that the following options are set:
- `Client Protocol` is `openid-connect`
- `Valid Redirect URIs` contains a list or URI for your application. Include `http://localhost:8000/` for development (**Important**: not recommended for production clients!)

#### Django Admin configuration

- Log into the Django admin interface (`http://localhost:8000/admin/` in development)
- Make sure the `Sites` contains an entry (should be done by the `migrate` command) and update them if you need to
- In the `Social Accounts` section, click `add` on `Social applications` and use the following settings
  - `Provider` => `Keycloak`
  - `Name` => `Keycloak` (could be anything)
  - `Client id` => The Client ID configured in your Keycloak Realm.
  - `Sites` => Make sure the site is added, otherwise you will run into `No providers available` errors.

### Adding a custom Navbar

You probably should override the navigation bar, so that it uses the logo of your own application and redirects to the correct view if you click on the logo.
This can be done by creating a template file in one of your apps. Check `integration/my_app/templates/astronauth/navbar.html`.

**Note**: Make sure that your app is above `astronauth` in the `INSTALLED_APPS` setting for this to work.

### Deployment

**TODO**
- example of hosting static files with nginx
- example of docker-compose with traefik as reverse proxy


## Contributing

This repository contains a minimal Django project for local development usage.

```bash
# Install as an editable package so changes are reflected immediately
pip install -e .
# then from the integration directory
cd integration
# Run the migrations
python manage.py migrate
# the app is then served via "http://localhost:8000/"
python manage.py runserver

# Follow the configuration steps mentioned above for adding a superuser and configuring a client.
```

### Code Format

The provided `tox.ini` files has a command `tox -e format` to format your code for you.

## Acknowledgements

**TODO** Determine which grants are applicable.
