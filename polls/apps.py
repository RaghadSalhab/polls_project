from django.apps import AppConfig
import time

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        from django.conf import settings
        if getattr(settings, "DEBUG", False):
            try:
                print("⏳ Waiting before run_setup...")
                time.sleep(2)
                from .messaging.core.setup_local_messaging import run_setup
                print("🚀 Running setup now...")
                # run_setup()
            except Exception as e:
                import traceback
                print("❌ Error in ready():", e)
                traceback.print_exc()