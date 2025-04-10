from .shared import env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',   # Use PostgreSQL as the backend
        'NAME': 'db',                                # Database name
        'USER': 'postgres',                          # Username
        'PASSWORD': 'gstools',                       # Password
        'HOST': '212.80.20.179',                       # Database host IP
        'PORT': '31028',                             # Port number
    }
}

