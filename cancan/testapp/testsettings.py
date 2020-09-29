import os
import random
import string
import environ

env = environ.Env()

DEBUG = True

ANONYMOUS_USER_NAME = "AnonymousUser"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.messages",
    "cancan",
    "cancan.testapp",
)

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "cancan.middleware.CanCanMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

CANCAN = {"ABILITIES": "cancan.testapp.abilities.get_abilities"}

# TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ROOT_URLCONF = "cancan.testapp.tests.urls"
SITE_ID = 1

SECRET_KEY = "".join([random.choice(string.ascii_letters) for x in range(40)])

# Database specific

# DATABASES = {'default': env.db(default="sqlite:///")}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "./test.db",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (os.path.join(os.path.dirname(__file__), "tests", "templates"),),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
