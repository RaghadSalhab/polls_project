
# polls/management/commands/start_consumers.py
from django.core.management.base import BaseCommand
from polls.messaging.consumers.consumer_manager import run_all_consumers

class Command(BaseCommand):
    help = "Start all SNS/SQS consumers for Questions, Choices, Users"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Starting all consumers..."))
        run_all_consumers()
