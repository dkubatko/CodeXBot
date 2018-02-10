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
COMMANDS_DEBUG = []
COMMANDS_DEBUG.extend(COMMANDS_AVAILABLE)
COMMAND_PREFIX = "command_"
