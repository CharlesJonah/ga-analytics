import os


class BaseConfig:
    """This class configures the parameters to be used across different enviroments"""

    SECRET_KEY = os.environ["SECRET_KEY"]
    PROJECT_ID = os.environ["PROJECT_ID"]
    GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
