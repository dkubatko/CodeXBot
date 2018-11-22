import sys
import socket
import requests
import bot_settings as settings
import threading
import time
import logging
import collections
from flask_socketio import SocketIO
from queue import Queue
from botCommands import Commands

class TwitchBot():
    def __init__(self, username, client_id, token, channel):
        self._log_setup()

        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.username = username

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        server = 'irc.chat.twitch.tv'
        port = 6667
        self.logger.info('Connecting to {0} on port {1}'.format(server, port))

        try:
            self.IRCconn = self._connect()
        except:
            self.logger.critical('Connection refused. Aborting')
            return

        self.logger.info('Conncetion successful')

        # Create message type
        self.Message = collections.namedtuple('Message', ['to', 'message'])

        # Set up messaging queue
        # TODO: Move to a separate function
        self._message_queue = Queue()
        self._message_thread = threading.Thread(target=self._message_queue_run)
        self._message_thread.daemon = True
        self._message_thread.start()

        self.logger.info('Setting up commands module')
        self.commands = Commands(self)

        self.logger.info('Initiating socketio to None')
        self._socketio = None
        self._sid = None


    def _log_setup(self):
        self.logger = logging.getLogger('bot')
        log_f = logging.FileHandler(settings.BOT_LOG_FILE)
        log_s = logging.StreamHandler()

        if (settings.DEBUG):
            self.logger.setLevel(logging.DEBUG)
            log_f.setLevel(logging.DEBUG)
            log_s.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(settings.LOG_FORMATTER)
        log_f.setFormatter(formatter)
        log_s.setFormatter(formatter)

        self.logger.addHandler(log_f)
        self.logger.addHandler(log_s)

    def _send(self, msg):
        if (not isinstance(msg, self.Message)):
            self.logger.error("{0} is not instance of message".format(msg))

        self.logger.info("Sending message {0}".format(msg))
        # If reciever is all, respond to all
        if (msg.to == 'ALL'):
            self.IRCconn.send(bytes(settings.MESSAGE_ALL.format(self.channel, msg.message), 'utf-8'))
        self.IRCconn.send(bytes(settings.MESSAGE_TO.format(self.channel, msg.to, msg.message), 'utf-8'))

    def add_to_message_queue(self, message):
        self._message_queue.put(message)

    def _message_queue_run(self, delay=1):
        self.logger.info('Starting message queue')
        while (True):
            msg = self._message_queue.get()
            self._send(msg)
            time.sleep(delay)

    def _connect(self):
        s = socket.socket()
        s.connect(('irc.chat.twitch.tv', 6667))

        s.send('PASS {}\r\n'.format(self.token).encode('utf-8'))
        s.send('NICK {}\r\n'.format(self.username).encode('utf-8'))

        # Request membership and commands usage
        s.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
        s.send('CAP REQ :twitch.tv/commands\r\n'.encode('utf-8'))

        s.send('JOIN {}\r\n'.format(self.channel).encode('utf-8'))

        return s

    def _process(self, line):
        print(line)
        parts = [elem.strip() for elem in line.split(' ')]

        # escape the case when no spaces
        if (len(parts) < 2):
            return

        # respond to ping message
        if ('PING' == parts[0]):
            self._on_ping()
            return

        # process privatemessage
        if ('PRIVMSG' == parts[1]):
            # escape the case when no message
            if (len(parts) < 3):
                return
            # extract sender name from line and put it in parts[2]
            parts[2] = parts[0].split('!')[0]
            # pass args with arg 0 as username
            self._on_prvmsg(parts[2:])


    def _on_prvmsg(self, args):
        # get sender with removed # from name
        sender = args[0][1:]
        # Remove : from message and join parts of the message
        message = ' '.join(args[1:])[1:]

        self.logger.debug('{0} sent message {1}'.format(sender, message))
        # if command
        if (message[0] == '!'):
            # extract command name w/o !
            cmd = message.split(' ')[0][1:]
            # extract all the args
            args = message.split(' ')[1:]
            self.commands.do(sender, cmd, args)
        return

    def _on_ping(self):
        self.IRCconn.send(bytes(settings.PONG_RESPONSE,'utf-8'))

    def start(self):
        self.logger.info("Starting connection to {0}".format(self.channel))
        s = self.IRCconn
        MODT = False
        readbuffer = ''
        while True:
            readbuffer = readbuffer + s.recv(1024).decode('utf-8')
            temp = readbuffer.split('\n')
            # Pops last empty message to readbuffer
            readbuffer = temp.pop()

            for line in temp:
                self._process(line)

    def set_socket(self, socketio, sid):
        self.logger.debug("Updating socket to new socket with sid: {0}".format(sid))
        self.commands.set_socket(socketio, sid)
        self._socketio = socketio
        self._sid = sid
