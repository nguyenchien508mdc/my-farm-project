import os

env = os.getenv("ENVIRONMENT", "dev").lower()

if env == "prod":
    from .prod import *
else:
    from .dev import *
