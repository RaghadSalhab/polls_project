import os
#defualt to local settings
env = os.getenv("DJANGO_ENV", "dev").lower() 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"my_poll_project.settings.{env}")

if env == "prod":
    from .prod import *
    print("⚙️ Loaded production settings")
elif env == "dev":
    from .dev import *
    print("⚙️ Loaded development (Docker) settings")
else:
    from .local import *
    print("⚙️ Loaded local settings")
