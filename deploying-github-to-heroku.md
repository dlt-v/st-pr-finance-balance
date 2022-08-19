# How to install a Django app to Heroku (without pain)

After spending 2 hours on watching weird tutorials, reading docs and so on I decided to make a quick and comprehensive guide on how to do what the title says. This guide was updated last on 17 of August 2022.

**We will be deploying our application via GitHub integration.** So be sure you have git repository already set.

## PIP Packages

First let's list what packages we'll need to get stuff working on Heroku.

1. [**gunicorn**](https://gunicorn.org/) - a Python WSGI HTTP Server. This thing is necessary for Heroku server to interface with our application.
2. [**whitenoise**](http://whitenoise.evans.io/en/stable/) - Heroku doesn't like static files, at all. So WhiteNoise takes care of that for us.
3. [**psycopg2-binary**](https://pypi.org/project/psycopg2-binary/) - Heroku by itself is not using LiteSQL and prefers to use its PostgreSQL database as default. This package is an adapter for our app.

Let's install our stuff:

```bash
pip install gunicorn whitenoise psycopg2-binary
```

After that remember to update/create your requirements.txt. This text file will tell Heroku which dependencies it needs to install in order to run our app.

```bash
pip freeze > requirements.txt
```

## Configuring Heroku itself

After you create your account on Heroku, create a new app and also make sure to install [**Heroku CLI**](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli) on your system. It'll help us quickly make environment variables and access settings of our app.

Open terminal and login into your Heroku account:

```
heroku login
```

Remember when I said that Heroku doesn't handle static files by itself? Yeah well, it will try do that and crash. We have WhiteNoise to solve this issue for us so we don't have to wrry about it. To save yourself a headache run this command:

```
heroku config:set DISABLE_COLLECTSTATIC=1 -a heroku_app_name
```

## Adding config files for Heroku

We told Heroku what dependencies it needs, but we still need to tell it a bit more. For example - our Python runtime version. If you're not sure which version you're working on, try this command:

```
python -v
```

Then create a file in your main directory called **runtime.txt** and insert your version. For me the file will look like this:

> python-3.10.2

And that's it for that file, next thing we have to do is to create a file without an extension called **Procfile**. It hass a command for our process worker to tell it what we want to do when the app is deployed. In it, also add just one line of code.

> web: gunicorn root.wsgi

Where "root" is the name of your root application.

## Settings.py part 1

Alright, so now we have to deal with how to serve static files with our new WhiteNoise middleware. Go to your **settings.py** file and import os package if you haven't done that already.

```python
import os
```

Go down to ALLOWED_HOSTS and fill it with the URL of your app. If you don't know what the URL Heroku has provided for you, you should find it when you click the "Open App" button in Heroku website.

For me this line will look like this:

```python
ALLOWED_HOSTS = ['127.0.0.1', 'st-pr-finance-balance.herokuapp.com']
```

Good, now a few lines below you should find INSTALLED_APPS, add your WhiteNoise app on top of it like so:

```python
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'login.apps.LoginConfig',
    'savings.apps.SavingsConfig',
    ...
]
```

We also need to add WhiteNoise to our MIDDLEWARE, as far as I read it, it's preferred to add it just below the security middleware and above everything else:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

Sticking with WhiteNoise for a moment, let's make sure we configured our static files correctly:

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Now let's migrate our newly installed apps to make sure it sticks and collect our static files in the specified location:

```
python manage.py migrate
```
```
python manage.py collectstatic
```

We will have to do one more thing in Settings.py but we'll have to do that after initially deploying our app to Heroku.

On Heroku, point the app to your GitHub repository and click Deploy. It shouldn't throw an error and you should see your app hosted. Unfortunately we're not there yet! If your app is using a database, you'll have to set it up still.

Thankfully now that we deployed it, in Heroku > Resources you should see "Heroku Postgres" under Add-ons. Click on it, then go to the database settings and then **Database Credentials**. You should see the login data that will allow your app to use it.

## Setting environment variables

Storing sensitive variables in our code is probably not a good idea, so we'll use environment variables for User and Password. In terminal run those following commands:

```
heroku config:set DB_USER=your_user_string -a heroku_app_name
```

```
heroku config:set DB_PASSWORD=your_password_string -a heroku_app_name
```

Also we can add an additional variable that will check if we're running stuff on Heroku and not locally:

```
heroku config:set IS_HEROKU=True -a heroku_app_name
```

To see if this worked, you can check it with this command:

```
heroku config -a heroku_app_name
```

## Settings.py part 2

We're on a finish line! Now let's connect our database using the new environment variables. Return to **settings.py** and let's fetch the variables first.

```python
import os
is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    db_user = os.environ.get('DB_USER')
    db_passwd = os.environ.get('DB_PASSWORD')
else:
    db_user = ''
    db_passwd = ''
```

The else clause is unnecessary but just in case someone runs it locally I wanted to include it.

Now go find DATABASES below and fill its information like so:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name_of_the_db',
        'USER': db_user,
        'PASSWORD': db_passwd,
        'HOST': 'host_address_of_the_db',
        'PORT': 'port_of_the_db',
    }
}
```

This is important, at first, locally, fill up your login data RAW. Do not commit changes for it, but instead run the migrate commmand:

```
python manage.py migrate
```

Now, after migrations are applied put the environment variables in their rightful place and commit.

TADA! You should have a working app on Heroku.
