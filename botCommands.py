import requests
import bot_settings as settings
import threading
import logging
import collections
from queue import Queue
from flask_socketio import SocketIO
import langdetect

class Commands():
    def __init__(self, bot):
        self._log_setup()

        self.bot = bot
        self.IRCconn = bot.IRCconn

        self.commands = {}

        # load commands from settings
        self._load_commands()

        # create command type
        self.Command = collections.namedtuple('Command', ['by', 'command', 'args'])

        # start command queue
        self._command_queue = Queue()
        self._command_thread = threading.Thread(target=self._command_queue_run)
        self._command_thread.daemon = True
        self._command_thread.start()

        # setting socketio sid var
        self._socketio = None
        self._sid = None

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
                self.logger.info("Loaded command <{0}>".format(cmd))
                self.commands[cmd] = getattr(self, settings.COMMAND_PREFIX + cmd)
            except AttributeError:
                self.logger.warning("<{0}> not found".format(cmd))


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
    def set_socket(self, socketio, sid):
        # self.logger.info("Socketio: {0} sid: {1}".format(socketio, sid))
        self._socketio = socketio
        self._sid = sid

    # Echoes text back to the chat
    def command_echo(self, cmd):
        return self.bot.Message(cmd.by, ' '.join(cmd.args))

    # Fowards text to the websocket
    def command_ask(self, cmd):
        self.logger.info("Starting {0} command".format(cmd.command))
        # check whether sid exists
        if (self._socketio == None):
            self.logger.debug("No socket set up.")
            return self.bot.Message(cmd.by,
                                    settings.COMMAND_FORWARD_RESPONSE_FAIL)

        message = ' '.join(cmd.args)
        try:
            lang = langdetect.detect_langs(message)
            if 'ru' in [l.lang for l in lang]:
                lang = 'ru'
            else:
                lang = 'en'
        except Exception as e:
            lang = 'none'

        data = {"message": message, "lang": lang}
        self._socketio("ask", data, room=self._sid)
        return self.bot.Message(cmd.by,
                                settings.COMMAND_FORWARD_RESPONSE_SUCCESS.format(message))


