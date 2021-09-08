import os


class BaseConfig:
    """This class configures the parameters to be used across different enviroments"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    PROJECT_ID = os.environ.get("PROJECT_ID")
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
