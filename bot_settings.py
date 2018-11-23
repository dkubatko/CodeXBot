# File with settings
DEBUG = True
# Const strings
COMMAND_NOT_FOUND = "Command {0} not found."

PONG_RESPONSE = "PONG :tmi.twitch.tv\r\n"

# Messaging templates
MESSAGE_ALL = 'PRIVMSG {0} :{1}\r\n'
MESSAGE_TO = 'PRIVMSG {0} :@{1} {2}\r\n'

# Bot setup
BOT_LOG_FILE = "bot.log"

# Commands setup
COMMANDS_LOG_FILE = "commands.log"
COMMANDS_AVAILABLE = ['echo']
COMMANDS_DEBUG = ['ask', 'giveaway']
COMMANDS_DEBUG.extend(COMMANDS_AVAILABLE)
COMMAND_PREFIX = "command_"

LOG_FORMATTER = '%(asctime)s / %(name)s / %(levelname)s\n'\
        '| FILE: %(filename)s FUNCTION: %(funcName)s LINE: %(lineno)d |\nMESSAGE: %(message)s'

COMMAND_FORWARD_RESPONSE_SUCCESS = "Forwarded message {0} to the socket."
COMMAND_FORWARD_RESPONSE_FAIL = "SID is not set yet. Connect to the server."

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