"""
Django settings for safe_client_config_service project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import environ
import django_stubs_ext

django_stubs_ext.monkeypatch()

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
print(ROOT_DIR)
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
DOT_ENV_FILE = env("DJANGO_DOT_ENV_FILE", default=None)
if READ_DOT_ENV_FILE or DOT_ENV_FILE:
    DOT_ENV_FILE = DOT_ENV_FILE or ".env"
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / DOT_ENV_FILE))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="random-dev-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default="true") == "true"

# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-ALLOWED_HOSTS
allowed_hosts = env("DJANGO_ALLOWED_HOSTS", default=".localhost,127.0.0.1,[::1]")
ALLOWED_HOSTS = [allowed_host.strip() for allowed_host in allowed_hosts.split(",")]

# Application definition

APPLICATION_VERSION = env("APPLICATION_VERSION", default="1.0.0")
APPLICATION_BUILD_NUMBER = env("APPLICATION_BUILD_NUMBER", default="1")

REST_FRAMEWORK = {
    # https://www.django-rest-framework.org/api-guide/renderers/
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
}

INSTALLED_APPS = [
    "corsheaders",
    "about.apps.AboutAppConfig",
    "chains.apps.AppsConfig",
    "safe_apps.apps.AppsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_yasg",
]

MIDDLEWARE = [
    "config.middleware.LoggingMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
    "safe-apps": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "short": {"format": "%(asctime)s %(message)s"},
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] [%(processName)s] %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "console_short": {
            "class": "logging.StreamHandler",
            "formatter": "short",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("ROOT_LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "LoggingMiddleware": {
            "handlers": ["console_short"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

ROOT_URLCONF = "config.urls"
FORCE_SCRIPT_NAME = env("FORCE_SCRIPT_NAME", default=None)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates/",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_NAME", default="config-db"),
        "USER": env("POSTGRES_USER", default="postgres"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="1112"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = "staticfiles"
STATIC_URL = "static/"

STATICFILES_DIRS = [
    "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "config.swagger_info.SAFE_CONFIG_SERVICE_SWAGGER_INFO"
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_URLS_REGEX = r"^/api/.*$"

CGW_URL = env("CGW_URL")
CGW_AUTH_TOKEN = env("CGW_AUTH_TOKEN")
CGW_SESSION_MAX_RETRIES = int(env("CGW_SESSION_MAX_RETRIES", default="0"))
CGW_SESSION_TIMEOUT_SECONDS = int(env("CGW_SESSION_TIMEOUT_SECONDS", default="2"))

# By default, Django stores files locally, using the MEDIA_ROOT and MEDIA_URL settings.
# (using the default the default FileSystemStorage)
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = f"{BASE_DIR}/media/"
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = env("MEDIA_URL", default="/media/")

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
# By default files with the same name will overwrite each other. Set this to False to have extra characters appended.
AWS_S3_FILE_OVERWRITE = True
# Setting AWS_QUERYSTRING_AUTH to False to remove query parameter authentication from generated URLs.
# This can be useful if your S3 buckets are public.
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = env(
    "DEFAULT_FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)

# SECURITY
# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins
allowed_csrf_origins = env("CSRF_TRUSTED_ORIGINS", default="")
if allowed_csrf_origins:
    CSRF_TRUSTED_ORIGINS = [
        allowed_csrf_origins.strip()
        for allowed_csrf_origins in allowed_csrf_origins.split(",")
    ]
