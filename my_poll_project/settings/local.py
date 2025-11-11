#settings/local.py
import os
import logging

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_poll_project.settings.dev'
from .dev import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_poll_project.settings.local'

LOCALSTACK_ENABLED = os.getenv("USE_LOCALSTACK", "True") == "True"


# Load environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Django settings
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])


import os


# DATABASES = {
#     'default': {
#         'ENGINE': 'django_prometheus.db.backends.mysql', 
#         'HOST': 'mysql_dev',
#         'PORT': '3306',     
#         'NAME': 'ms1_db',
#         'USER': os.getenv('DB_USER', 'root'),   
#         'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
#     },
#     'ms2_db': {
#         'ENGINE': 'django_prometheus.db.backends.mysql',
#         'HOST': 'mysql_dev',
#         'PORT': '3306',       # البورت الداخلي للحاوية
#         'NAME': 'ms2_db',
#         'USER': os.getenv('DB_USER', 'root'),
#         'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # أو django_prometheus.db.backends.mysql
        'HOST': 'mysql_local',    # أو localhost لو خارج الـ container
        'PORT': '3306',
        'NAME': 'polls_db',
        'USER': 'root',
        'PASSWORD': 'root',       # <=== لازم يكون هنا
    },
    'ms2_db': {
        'ENGINE': 'django_prometheus.db.backends.mysql',
        'HOST': 'mysql_dev',
        'PORT': '3306',
        'NAME': 'ms2_db',
        'USER': os.getenv('DATABASE_USER', 'root'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'root'),
    }
}

SLACK_TOKEN = ''
ASYNC_STARTUP_THREADS = []

print("✅ Local settings loaded successfully (LocalStack mode = {})".format(LOCALSTACK_ENABLED))
