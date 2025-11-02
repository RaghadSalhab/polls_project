#settings/dev.py
from .base import *
import os
import environ
from pathlib import Path

# my_poll_project/settings/dev.py
import os
DEBUG = True
ALLOWED_HOSTS = ['*']  

# Example API URLs
RAGHAD_API_BASE_URL = "http://core-api.dev-core-api.svc.cluster.local"
TEAM_SCHEDULING_BASE_URL = "http://team-scheduling.dev-core-api.svc.cluster.local"

# AWS resources
AWS = {
    "SQS": {
        "TEAM_RECOGNITION": {
            "RECOGNITION_UPDATES": "prod-team-recognition-updates",
            "RECOGNITION_UPDATES_BALMM": "prod-team-recognition-updates-balmm"
        },
        "QUERY_EXECUTOR": "prod-query-executor-queue"
    },
    "SNS": {
        "NOTIFICATIONS": "arn:aws:sns:us-east-1:123456789012:prod-team-recognition-notifications"
    }
}


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


# External integrations
SLACK_TOKEN = "xoxb-prod-token"
ASYNC_STARTUP_THREADS = ["aws_sqs_thread"]
