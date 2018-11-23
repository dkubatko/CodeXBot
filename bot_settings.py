import os

# File with settings
DEBUG = True
# Const strings
COMMAND_NOT_FOUND = "Command {0} not found."

PONG_RESPONSE = "PONG :tmi.twitch.tv\r\n"

# Messaging templates
MESSAGE_ALL = 'PRIVMSG {0} :{1}\r\n'
MESSAGE_TO = 'PRIVMSG {0} :@{1} {2}\r\n'

# Logs directory
LOG_DIR = "logs/"

# Bot setup
BOT_LOG_FILE = LOG_DIR + "bot.log"

# Commands setup
COMMANDS_LOG_FILE = LOG_DIR + "commands.log"
COMMANDS_AVAILABLE = ['echo']
COMMANDS_DEBUG = ['ask', 'giveaway']
COMMANDS_DEBUG.extend(COMMANDS_AVAILABLE)
COMMAND_PREFIX = "command_"

LOG_FORMATTER = '%(asctime)s / %(name)s / %(levelname)s\n'\
        '| FILE: %(filename)s FUNCTION: %(funcName)s LINE: %(lineno)d |\nMESSAGE: %(message)s'

COMMAND_FORWARD_RESPONSE_SUCCESS = "Forwarded message {0} to the socket."
COMMAND_FORWARD_RESPONSE_FAIL = "SID is not set yet. Connect to the server."

# DB setup
DB_CONNECTION_STRING = "mongodb+srv://{0}:{1}@codexbot-cluster-ds4ut.mongodb.net/test?retryWrites=true"
DB_LOG_FILE = LOG_DIR + "db.log"

# Get environment variables
try:
    DB_USERNAME = os.environ['DB_USERNAME']
    DB_PASSWORD = os.environ['DB_PASSWORD']
except:
    print("Environment variables are not set up properly. Aborting.")
    exit()

# VK music display settings
VK_ACCESS_TOKEN_LINK = "https://oauth.vk.com/access_token"
VK_API_LINK = "https://api.vk.com/method/"
VK_API_VERSION = '5.92'
VK_NO_AUDIO = "No audio playing. Check status broadcasting"
VK_LOG_FILE = LOG_DIR + "vkmd.log"
VK_MUSIC_OUT_FILE = "now_playing.txt"
VK_STATUS_POLL_DELAY = 3
try:
    VK_CLIENT_ID = os.environ['VK_CLIENT_ID']
    VK_CLIENT_SECRET = os.environ['VK_CLIENT_SECRET']
    VK_REDIRECT_URI = os.environ['VK_REDIRECT_URI']
except:
    print("Environment variables are not set up properly. Aborting.")
    exit()

# Moderators list
MODERATORS = ['drazzzer']

# Giveaway args settings
GIVEAWAY_MOD_ARGS = ['start', 'close']
GIVEAWAY_ARGS = ['stats']
GIVEAWAY_START_USAGE = "Usage: <!giveaway start> <name> <description>"
GIVEAWAY_NO_ARG = "No such argument for <!giveaway> command"

# Commands constants
GIVEAWAY_DEFAULT_NAME = "Default giveaway"
GIVEAWAY_DEFAULT_DESCRIPTION = "Default giveaway"
GIVEAWAY_STATUS_LIVE = "Giveaway <{0}: {1}> is live!"
GIVEAWAY_ALREADY_LIVE = "Giveaway <{0}> is already live. Close it to start a new one."
GIVEAWAY_STATUS_OFF = "No giveaways are up yet. Stay tuned!"
GIVEAWAY_INFO = "{0}: {1}"
GIVEAWAY_NEW_ENTRY = "You entered giveaway <{0}>!"
GIVEAWAY_ALREADY_REGISTERED = "You have already registered for giveaway {0}"
GIVEAWAY_CLOSED = "Giveaway <{0}> has been closed"
GIVEAWAY_STATS = "Giveaway <{0}> | Entries: {2} | Participants: {3}"