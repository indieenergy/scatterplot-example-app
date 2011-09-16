DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'scatterplot',                # Or path to database file if using sqlite3.
        'USER': 'root',                         # Not used with sqlite3.
        'PASSWORD': 'db.123',                   # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


API_HOST = "indiegeopod.com"

GEOPOD_CONSUMER_KEY = 'kZxbgkwBqbAyvC9dLe'
GEOPOD_CONSUMER_SECRET = 'nyEyz6eMgEqrvKE2H7Q42rTHUQthYqhM'

