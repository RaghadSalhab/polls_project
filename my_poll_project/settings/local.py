#settings/local.py
import os
import logging

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_poll_project.settings.dev'
from .dev import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_poll_project.settings.local'

LOCALSTACK_ENABLED = os.getenv("USE_LOCALSTACK", "True") == "True"


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Django settings
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME", default="polls_db"),
        'USER': env("DATABASE_USER", default="postgres"),
        'PASSWORD': env("DATABASE_PASSWORD", default="1234"),
        'HOST': env("DATABASE_HOST", default="host.docker.internal"),
        'PORT': env("DATABASE_PORT", default="5432"),
    }
}

if LOCALSTACK_ENABLED:
    print("🔄 Redirecting all *_BASE_URL to LocalStack (http://localhost:4566) ...")

    for key, value in list(globals().items()):
        if key.endswith('_BASE_URL') and isinstance(value, str):
            if 'svc.cluster.local' in value or 'amazonaws.com' in value:
                service_name = value.split('.')[0].split('//')[-1]
                globals()[key] = f"http://localhost:4566/{service_name}"


SLACK_TOKEN = ''
ASYNC_STARTUP_THREADS = []

print("✅ Local settings loaded successfully (LocalStack mode = {})".format(LOCALSTACK_ENABLED))
