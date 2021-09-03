import os

from config import config


environment = os.environ["ENVIRONMENT"] or "development"
config = config[environment]
