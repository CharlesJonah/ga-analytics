import os

from config import config


environment = os.environ.get("ENVIRONMENT", "development")
config = config[environment]
