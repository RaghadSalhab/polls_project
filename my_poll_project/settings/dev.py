#settings/dev.py
from .base import *
import os
import environ
from pathlib import Path

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

# LocalStack / AWS for Dev
LOCALSTACK_ENDPOINT = env("LOCALSTACK_ENDPOINT", default="http://localstack:4566")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="test")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="test")
AWS_DEFAULT_REGION = env("AWS_DEFAULT_REGION", default="us-east-1")

# Redis
REDIS_HOST = env("REDIS_HOST", default="host.docker.internal")
REDIS_PORT = env("REDIS_PORT", default=6380)
REDIS_DB = env("REDIS_DB", default=0)
REDIS_PASSWORD = env("REDIS_PASSWORD", default="")
REDIS_MAX_CONNECTIONS = env("REDIS_MAX_CONNECTIONS", default=50)

AWS = {
    'SQS': {
        'NOTIFICATION_QUEUE': 'user-notifications',
        'PROCESS_QUEUE': 'image-processing',
        'DEAD_LETTER_QUEUE': 'dlq-main'
    },
    'S3': {
        'UPLOADS_BUCKET': 'user-uploads',
        'BACKUP_BUCKET': 'app-backups'
    },
    'SNS': {
        'ALERTS_TOPIC': 'system-alerts'
    },
    "KINESIS": {
        "STREAMS": {
            "DEV_STREAM": "dev-data-stream",
            "TEAM_RECOGNITION_STREAM": "team-recognition-stream"
        }
    },
}
