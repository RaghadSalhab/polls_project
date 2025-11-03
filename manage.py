
# """Django's command-line utility for administrative tasks."""
# import os
# import sys
# import boto3

# def main():
#     """Run administrative tasks."""
#     env = os.getenv("DJANGO_ENV", "local").lower()
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"my_poll_project.settings.{env}")
#     from django.core.management import execute_from_command_line
#     execute_from_command_line(sys.argv)

# if __name__ == '__main__':
#     main()
import os
import sys
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    env = os.getenv("DJANGO_ENV", "local").lower()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"my_poll_project.settings.{env}")

    role = os.getenv("ROLE", "PUBLISHER").upper()
    os.environ.setdefault("APP_ROLE", role)

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
