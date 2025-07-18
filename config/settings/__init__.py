import os

env = os.getenv("DJANGO_ENV", "dev")  # default là dev

if env == "prod":
    from .prod import *
elif env == "test":
    from .test import *
else:
    from .dev import *