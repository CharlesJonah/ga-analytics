import os


class BaseConfig:
    """This class configures the parameters to be used across different enviroments"""

    SECRET_KEY = os.environ["SECRET_KEY"]
