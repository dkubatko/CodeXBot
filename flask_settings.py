import logging
import os
from flask import request
DEBUG = True

# Formatter for events
class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)

# Logs directory
LOG_DIR = "logs/"

# Logging settings
REQUEST_FORMAT = '%(asctime)s / %(name)s / %(levelname)s\n'\
        '| FROM: %(remote_addr)s REQUEST URL: %(url)s |\n'\
        '| FILE: %(filename)s FUNCTION: %(funcName)s LINE: %(lineno)d |\nMESSAGE: %(message)s'

FLASK_APP_LOG_FORMAT = '%(asctime)s / %(name)s / %(levelname)s\n'\
        '| FILE: %(filename)s FUNCTION: %(funcName)s LINE: %(lineno)d |\nMESSAGE: %(message)s'
FLASK_LOG_FILE = LOG_DIR + 'flask_app.log'

VK_REDIRECT_URI_LOCAL = "http://127.0.0.1:5000/vk"
VK_REDIRECT_URI_REMOTE = "http://192.168.1.25:5000/vk"

BASE_URI_LOCAL = "http://127.0.0.1:5000"
BASE_URI_REMOTE = "http://192.168.1.25:5000"

# Get environment variables
try:
    BOT_USERNAME = os.environ['CODEXBOT_USERNAME']
    BOT_CLIENT_ID = os.environ['CODEXBOT_CLIENT_ID']
    BOT_TOKEN = os.environ['CODEXBOT_TOKEN']
except:
    print("Environment variables are not set up properly. Aborting.")
    exit()
