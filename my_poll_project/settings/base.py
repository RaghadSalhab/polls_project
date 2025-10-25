# Django settings for my_poll_project.
#settings/base.py
from pathlib import Path
import os
import environ
from datetime import timedelta
from ddtrace import tracer

BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="django-insecure-placeholder")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'polls',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'polls.middleware.SQLAlchemyRequestIDMiddleware',
]

ROOT_URLCONF = 'my_poll_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_poll_project.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework config
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Datadog Tracer
tracer.set_tags({"project": "polls_app"})

# AWS mock (LocalStack)
AWS = {
    "SQS": {
        "QUESTION": {
            "QUESTION_QUEUE": "http://localhost:4566/000000000000/question-queue",
            "QUESTION_DLQ": "http://localhost:4566/000000000000/question-dlq",
        },
        "CHOICE": {
            "CHOICE_QUEUE": "http://localhost:4566/000000000000/choice-queue",
            "CHOICE_DLQ": "http://localhost:4566/000000000000/choice-dlq",
        },
        "USER": {
            "USER_QUEUE": "http://localhost:4566/000000000000/user-queue",
            "USER_DLQ": "http://localhost:4566/000000000000/user-dlq",
        },
        "STATS": {
            "STATS_QUEUE": "http://localhost:4566/000000000000/stats-queue",
            "STATS_DLQ": "http://localhost:4566/000000000000/stats-dlq",
        },
    },
    "SNS": {
        "QUESTION_TOPIC": "arn:aws:sns:us-east-1:000000000000:question-topic",
        "CHOICE_TOPIC": "arn:aws:sns:us-east-1:000000000000:choice-topic",
        "USER_TOPIC": "arn:aws:sns:us-east-1:000000000000:user-topic",
        "STATS_TOPIC": "arn:aws:sns:us-east-1:000000000000:stats-topic",
    },
}
