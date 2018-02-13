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
COMMANDS_DEBUG = ['ask']
COMMANDS_DEBUG.extend(COMMANDS_AVAILABLE)
COMMAND_PREFIX = "command_"

LOG_FORMATTER = '%(asctime)s / %(name)s / %(levelname)s\n'\
        '| FILE: %(filename)s FUNCTION: %(funcName)s LINE: %(lineno)d |\nMESSAGE: %(message)s'

COMMAND_FORWARD_RESPONSE_SUCCESS = "Forwarded message {0} to the socket."
COMMAND_FORWARD_RESPONSE_FAIL = "SID is not set yet. Connect to the server."
