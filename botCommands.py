import requests
import bot_settings as settings
import threading
import logging
import collections
from giveaway import Giveaway
from queue import Queue
from flask_socketio import SocketIO
from textblob import TextBlob

class Commands():
    def __init__(self, bot):
        self._log_setup()

        self.bot = bot
        self.IRCconn = bot.IRCconn

        self.commands = {}

        # load commands from settings
        self._load_commands()

        # create command type
        # TODO: move to class
        self.Command = collections.namedtuple('Command', ['by', 'command', 'args'])

        # start command queue
        self._command_queue = Queue()
        self._command_thread = threading.Thread(target=self._command_queue_run)
        self._command_thread.daemon = True
        self._command_thread.start()

        # setting socketio sid var
        self._emit = None
        self._sid = None

        # setting moderators
        # TODO: Convert to class
        self.moderators = []
        self._load_moderators()

        # initiate giveaway class
        self.giveaway = Giveaway(self.logger)

    def _log_setup(self):
        self.logger = logging.getLogger('bot.commands')
        log_f = logging.FileHandler(settings.COMMANDS_LOG_FILE)

        if (settings.DEBUG):
            self.logger.setLevel(logging.DEBUG)
            log_f.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(settings.LOG_FORMATTER)
        log_f.setFormatter(formatter)

        self.logger.addHandler(log_f)

    def _load_commands(self):
        cmdlist = settings.COMMANDS_AVAILABLE
        # load debug commands if DEBUG is true
        if (settings.DEBUG):
            cmdlist = settings.COMMANDS_DEBUG

        for cmd in cmdlist:
            try:
                self.commands[cmd] = getattr(self, settings.COMMAND_PREFIX + cmd)
                self.logger.info("Loaded command <{0}>".format(cmd))
            except AttributeError:
                self.logger.warning("<{0}> not found".format(cmd))

    def _load_moderators(self):
        self.moderators = settings.MODERATORS


    # performs one command at a time
    def _command_queue_run(self):
        self.logger.info("Starting command queue")
        while (True):
            cmd = self._command_queue.get()
            self.logger.info("Executing <{0}>".format(cmd))
            self._perform(cmd)

    # Performs command with args
    def _perform(self, cmd):
        # find command key in the list
        if (cmd.command in self.commands.keys()):
            # call handling function
            resp = self.commands[cmd.command](cmd)
            # if response is a message, add it to the message queue
            if (isinstance(resp, self.bot.Message)):
                self.logger.info("Adding <{0}> to the message queue".format(resp))
                self.bot.add_to_message_queue(resp)
        else:
            self.logger.info(settings.COMMAND_NOT_FOUND.format(cmd))

    # puts command in the command queue
    def do(self, by, command, args):
        cmd = self.Command(by, command, args)
        self._add_to_command_queue(cmd)

    # Adds command to the command queue
    def _add_to_command_queue(self, cmd):
        self.logger.info("Adding <{0}> to the command queue".format(cmd))
        self._command_queue.put(cmd)

    # updates socket to new sid
    def set_socket(self, emit_func, sid):
        # self.logger.info("Socketio: {0} sid: {1}".format(socketio, sid))
        self._emit = emit_func
        self._sid = sid

    # Checks for a user moderator status
    # TODO: Twitch API
    def check_mod(self, username):
        if username in self.moderators:
            return True
        else:
            return False

    # Echoes text back to the chat
    def command_echo(self, cmd):
        return self.bot.Message(cmd.by, ' '.join(cmd.args))

    # Fowards text to the websocket
    def command_ask(self, cmd):
        self.logger.info("Starting {0} command".format(cmd.command))
        # check whether sid exists
        if (self._sid == None):
            self.logger.debug("No socket set up.")
            return self.bot.Message(cmd.by,
                                    settings.COMMAND_FORWARD_RESPONSE_FAIL)

        message = ' '.join(cmd.args)
        try:
            lang = TextBlob(message).detect_language()
            if 'ru' == lang:
                lang = 'ru'
            else:
                lang = 'en'
        except Exception as e:
            lang = 'none'

        data = {"message": message, "lang": lang}
        self._emit("ask", data, room=self._sid)
        return self.bot.Message(cmd.by,
                                settings.COMMAND_FORWARD_RESPONSE_SUCCESS.format(message))


    # givaway operations
    def command_giveaway(self, cmd):
        if len(cmd.args) == 0:
            arg = None
        else:
            arg = cmd.args[0]
        
        # Check whether command requires mod access
        if arg in settings.GIVEAWAY_MOD_ARGS:
            if self.check_mod(cmd.by):
                return self._cmd_giveaway_mods(cmd)      
        else:
            return self._cmd_giveaway(cmd)

    # Giveaway handler for moderators
    def _cmd_giveaway_mods(self, cmd):
        if len(cmd.args) == 0:
            arg = None
        else:
            arg = cmd.args[0]

        if arg == 'start':
            # check for arguments presence
            if len(cmd.args) < 3:
                return self.bot.Message(cmd.by, 
                    settings.GIVEAWAY_START_USAGE)
            # Get arguments from the command call
            name = cmd.args[1]
            description = cmd.args[2]
            # Execute command
            success, message = self.giveaway.start(name, description)

            # Send event success of giveaway start
            if success:
                data = {"message": 'Giveaway started', "lang": 'en'}
                self._emit("giveaway", data, room=self._sid)

            return self.bot.Message(cmd.by, message)
        elif arg == 'close':
            success, message = self.giveaway.close()

            # Send event success of giveaway close
            if success:
                data = {"message": 'Giveaway closed', "lang": 'en'}
                self._emit("giveaway", data, room=self._sid)

            return self.bot.Message(cmd.by, message)
        else:
            return self.bot.Message(cmd.by, 
                    settings.GIVEAWAY_NO_ARG)


    # Giveaway handler for non-mod users
    def _cmd_giveaway(self, cmd):
        if len(cmd.args) == 0:
            arg = None
        else:
            arg = cmd.args[0]
        
        # Check for requested argument
        if not arg:
            success, message = self.giveaway.enter(cmd.by)

            # Send event success of giveaway entry
            if success:
                data = {"message": '{0} entered giveaway'.format(cmd.by), 
                                "lang": 'en'}
                self._emit("giveaway", data, room=self._sid)

            return self.bot.Message(cmd.by, message)
        elif arg == 'stats':
            success, message = self.giveaway.statistics()
            return self.bot.Message(cmd.by, message)
        elif arg == 'info':
            success, message = self.giveaway.info()
            return self.bot.Message(cmd.by, message)
        else:
            return self.bot.Message(cmd.by, 
                settings.GIVEAWAY_NO_ARG)
