from flask import Flask

from constants import config

application = Flask(__name__)

application.config.from_object(config)
